# Setup 

**Installation**
```python
! git clone https://github.com/goin2crazy/gitrag
%cd gitrag
! pip install -q -r requirements.txt
```

**Load Model** 
```python
from pipeline import Main 

# There is example "goin2crazy" is github username
# You can write instead whatever you want 
mainbro = Main('goin2crazy', model='gemini')
```

**Run** 
```python
mainbro('[YOUR REQUEST/QUESTION]')
```
