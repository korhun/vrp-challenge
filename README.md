# vrp-challenge
## run
```bash
    # install requirements
    pip install -r ./requirements.txt
    cd vrp
```
### brute force
```bash
    # unlimited capacity
    python core.py -s bruteforce
    
    # limited capacity
    python core.py -s bruteforce -l
    
    # limited capacity with verbose
    python core.py -s bruteforce -l -v        
```

### alternative run
```bash
    python core.py --style <style> --filename <input filename (optional)> --limited_capacity --verbose 
    # or
    python core.py -s <style> -f <input filename (optional)> -l -v
```
## styles
* bruteforce
