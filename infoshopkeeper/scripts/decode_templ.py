import os

for root, dirs, files in os.walk('.'):             
     for fil in files:
         if fil.endswith('Template.py') or fil.endswith('Skeleton.py'):
            try:                        
                with open(os.path.join(root,fil), 'r') as f:
                     data = f.read()
                     data = eval(data)
                     data = data.decode('unicode_escape')
                with open(os.path.join(root,fil), 'w') as f:
                     f.write(data)
            except:
                pass
