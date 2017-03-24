## {{{ http://code.activestate.com/recipes/501154/ (r2)
#made to operate as a regular queue 12/1/2011 Markos Kapes

import os, sys, marshal, glob, _thread
from time import time as _time
try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading
    
# Filename used for index files, must not contain numbers
INDEX_FILENAME = 'index'

# Exception thrown when calling get() on an empty queue
class Empty(Exception):  pass

class PersistentQueue:

    def __init__(self, name, cache_size=512, marshal=marshal, maxsize=0):
        """
        Create a persistent FIFO queue named by the 'name' argument.

        The number of cached queue items at the head and tail of the queue
        is determined by the optional 'cache_size' parameter.  By default
        the marshal module is used to (de)serialize queue items, but you
        may specify an alternative serialize module/instance with the
        optional 'marshal' argument (e.g. pickle).
        """
        assert cache_size > 0, 'Cache size must be larger than 0'
        self.name = name
        try:
            os.makedirs(name)
        except Exception:
            pass
        self.cache_size = cache_size
        self.marshal = marshal
        self.maxsize=maxsize
        self.index_file = os.path.join(name, INDEX_FILENAME)
        self.temp_file = os.path.join(name, 'tempfile')        
        self.mutex = _threading.RLock()
        self.not_full = _threading.Condition(self.mutex)
        self.not_empty = _threading.Condition(self.mutex)
        self.all_tasks_done = _threading.Condition(self.mutex)
        self._init_index()
        self.unfinished_tasks = self.qsize()   

    def _init_index(self):
        if not os.path.exists(self.name):
            os.mkdir(self.name)
        if os.path.exists(self.index_file):
            index_file = open(self.index_file)
            self.head, self.tail = [int(x) for x in index_file.read().split(' ')]
            index_file.close()
        else:
            self.head, self.tail = 0, 1
        def _load_cache(cache, num):
            name = os.path.join(self.name, str(num))
            mode = 'rb+' if os.path.exists(name) else 'wb+'
            cachefile = open(name, mode)
            try:
                setattr(self, cache, self.marshal.load(cachefile))
            except EOFError:
                setattr(self, cache, [])
            cachefile.close()
        _load_cache('put_cache', self.tail)
        _load_cache('get_cache', self.head)
        assert self.head < self.tail, 'Head not less than tail'

    def _sync_index(self):
        assert self.head < self.tail, 'Head not less than tail'
        index_file = open(self.temp_file, 'w')
        index_file.write('%d %d' % (self.head, self.tail))
        index_file.close()
        if os.path.exists(self.index_file):
            os.remove(self.index_file)
        os.rename(self.temp_file, self.index_file)

    def _split(self):
        put_file = os.path.join(self.name, str(self.tail))
        temp_file = open(self.temp_file, 'wb')
        self.marshal.dump(self.put_cache, temp_file)
        temp_file.close()
        if os.path.exists(put_file):
            os.remove(put_file)
        os.rename(self.temp_file, put_file)
        self.tail += 1
        if len(self.put_cache) <= self.cache_size:
            self.put_cache = []
        else:
            self.put_cache = self.put_cache[:self.cache_size]
        self._sync_index()

    def _join(self):
        current = self.head + 1
        if current == self.tail:
            self.get_cache = self.put_cache
            self.put_cache = []
        else:
            get_file = open(os.path.join(self.name, str(current)), 'rb')
            self.get_cache = self.marshal.load(get_file)
            get_file.close()
            try:
                os.remove(os.path.join(self.name, str(self.head)))
            except:
                pass
            self.head = current
        if self.head == self.tail:
            self.head = self.tail - 1
        self._sync_index()

    def _sync(self):
        self.unfinished_tasks=self.qsize()
        self._sync_index()
        get_file = os.path.join(self.name, str(self.head))
        temp_file = open(self.temp_file, 'wb')
        self.marshal.dump(self.get_cache, temp_file)
        temp_file.close()
        if os.path.exists(get_file):
            os.remove(get_file)
        os.rename(self.temp_file, get_file)
        put_file = os.path.join(self.name, str(self.tail))
        temp_file = open(self.temp_file, 'wb')
        self.marshal.dump(self.put_cache, temp_file)
        temp_file.close()
        if os.path.exists(put_file):
            os.remove(put_file)
        os.rename(self.temp_file, put_file)

    def __len__(self):
        """
        Return number of items in queue.
        """
        self.mutex.acquire()
        try:
            return (((self.tail-self.head)-1)*self.cache_size) + \
                    len(self.put_cache) + len(self.get_cache)
        finally:
            self.mutex.release()

    def _put(self, obj):
        """
        Put the item 'obj' on the queue.
        """
        self.mutex.acquire()

        try:
            self.put_cache.append(obj)
            if len(self.put_cache) >= self.cache_size:
                self._split()
        finally:
            self.mutex.release()

    def _get(self):
        """
        Get an item from the queue.
        Throws Empty exception if the queue is empty.
        """
        self.mutex.acquire()
        try:
            if len(self.get_cache) > 0:
                return self.get_cache.pop(0)
            else:
                self._join()
                if len(self.get_cache) > 0:
                    return self.get_cache.pop(0)
                else:
                    raise Empty
        finally:
            self.mutex.release()

    def _qsize(self):
        """Return the approximate size of the queue (not reliable!)."""
        n = self.__len__()
        return n

    def qsize(self):
        """Return the approximate size of the queue (not reliable!)."""
        n = self._qsize()
        return n

    def task_done(self):
        """Indicate that a formerly enqueued task is complete.

        Used by Queue consumer threads.  For each get() used to fetch a task,
        a subsequent call to task_done() tells the queue that the processing
        on the task is complete.

        If a join() is currently blocking, it will resume when all items
        have been processed (meaning that a task_done() call was received
        for every item that had been put() into the queue).

        Raises a ValueError if called more times than there were items
        placed in the queue.
        """
        self.all_tasks_done.acquire()
        try:
            unfinished = self.unfinished_tasks - 1
            if unfinished <= 0:
                if unfinished < 0:
                    raise ValueError('task_done() called too many times')
                self.all_tasks_done.notify_all()
            self.unfinished_tasks = unfinished
        finally:
            self._sync()
            print(self.unfinished_tasks, self.qsize()) 
            self.all_tasks_done.release()

    def join(self):
        """Blocks until all items in the Queue have been gotten and processed.

        The count of unfinished tasks goes up whenever an item is added to the
        queue. The count goes down whenever a consumer thread calls task_done()
        to indicate the item was retrieved and all work on it is complete.

        When the count of unfinished tasks drops to zero, join() unblocks.
        """
        self.all_tasks_done.acquire()
        try:
            print("qsize: ", self.qsize(), " unfinished_tasks: ", self.unfinished_tasks)
            while self.unfinished_tasks:
                self.all_tasks_done.wait()
        finally:
            self.all_tasks_done.release()

    def sync(self):
        """
        Synchronize memory caches to disk.
        """
        self.mutex.acquire()
        try:
            self._sync()
        finally:
            self.mutex.release()

    def empty(self):
        """Return True if the queue is empty, False otherwise (not reliable!)."""
        self.mutex.acquire()
        n = not self._qsize()
        self.mutex.release()
        return n

    def full(self):
        """Return True if the queue is full, False otherwise (not reliable!)."""
        self.mutex.acquire()
        n = 0 < self.maxsize == self._qsize()
        self.mutex.release()
        return n

    def put(self, item, block=True, timeout=None):
        """Put an item into the queue.

        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until a free slot is available. If 'timeout' is
        a positive number, it blocks at most 'timeout' seconds and raises
        the Full exception if no free slot was available within that time.
        Otherwise ('block' is false), put an item on the queue if a free slot
        is immediately available, else raise the Full exception ('timeout'
        is ignored in that case).
        """
        self.not_full.acquire()
        try:
            if self.maxsize > 0:
                if not block:
                    if self._qsize() == self.maxsize:
                        raise Full
                elif timeout is None:
                    while self._qsize() == self.maxsize:
                        self.not_full.wait()
                elif timeout < 0:
                    raise ValueError("'timeout' must be a positive number")
                else:
                    endtime = _time() + timeout
                    while self._qsize() == self.maxsize:
                        remaining = endtime - _time()
                        if remaining <= 0.0:
                            raise Full
                        self.not_full.wait(remaining)
            self._put(item)
            self.unfinished_tasks += 1
            self.not_empty.notify()
        finally:
            self.not_full.release()

    def put_nowait(self, item):
        """Put an item into the queue without blocking.

        Only enqueue the item if a free slot is immediately available.
        Otherwise raise the Full exception.
        """
        return self.put(item, False)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until an item is available. If 'timeout' is
        a positive number, it blocks at most 'timeout' seconds and raises
        the Empty exception if no item was available within that time.
        Otherwise ('block' is false), return an item if one is immediately
        available, else raise the Empty exception ('timeout' is ignored
        in that case).
        """
        self.not_empty.acquire()
        try:
            if not block:
                if not self._qsize():
                    raise Empty
            elif timeout is None:
                while not self._qsize():
                    self.not_empty.wait()
            elif timeout < 0:
                raise ValueError("'timeout' must be a positive number")
            else:
                endtime = _time() + timeout
                while not self._qsize():
                    remaining = endtime - _time()
                    if remaining <= 0.0:
                        raise Empty
                    self.not_empty.wait(remaining)
            item = self._get()
            self.not_full.notify()
            return item
        finally:
            self.not_empty.release()

    def get_nowait(self):
        """Remove and return an item from the queue without blocking.

        Only get an item if one is immediately available. Otherwise
        raise the Empty exception.
        """
        return self.get(False)

    def close(self):
        """
        Close the queue.  Implicitly synchronizes memory caches to disk.
        No further accesses should be made through this queue instance.
        """
        self.mutex.acquire()
        try:
            self._sync()
            if os.path.exists(self.temp_file):
                try:
                    os.remove(self.temp_file)
                except:
                    pass
        finally:
            self.mutex.release()

## Tests
if __name__ == "__main__":
    ELEMENTS = 1000
    p = PersistentQueue('test', 10)
    print('Enqueueing %d items, cache size = %d to queue of size: %s' % (ELEMENTS, p.cache_size, p.qsize()))
    for a in range(ELEMENTS):
        p.put(str(a))
    print('%d elements enqueued' % ELEMENTS)
    p.sync()
    print('Queue length (using __len__):', len(p))
    print('Dequeueing %d items' % (ELEMENTS/2))
    for a in range(ELEMENTS/2):
        p.get()
    print('Queue length (using __len__):', len(p))
    print('Dequeueing %d items' % (ELEMENTS/2))
    for a in range(ELEMENTS/2):
        p.get()
    print('Queue length (using __len__):', len(p))
    p.sync()
    print('Enqueueing %d items, cache size = %d to queue of size: %s' % (ELEMENTS, p.cache_size, p.qsize()))
    for a in range(ELEMENTS):
        p.put(str(a))
    print('%d elements enqueued' % ELEMENTS)
    p.sync()
    
    class MyThread( _threading.Thread ):
        def __init__(self, queue):
            _threading.Thread.__init__(self)
            self.queue=queue
    
        def run(self):
            print('Queue length (using __len__):', len(self.queue))
            isDone=False
            while not isDone:
                self.queue.get()
                self.queue.task_done()
                print(self.queue.qsize(), len(self.queue))
                if self.queue.qsize() == 0:
                    isDone=True
                
            print('Queue length (using __len__):', len(self.queue), self.queue.__len__())
    
    t=MyThread(p)
    t.setDaemon(True)
    t.start()
    print("joining queue of size: ", p.qsize(), " and unfinished tasks size: ", p.unfinished_tasks)
    p.join()
    print("p.finished")
    p.close()
## end of http://code.activestate.com/recipes/501154/ }}}
