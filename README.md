# vrp-challenge
## run
```bash
    # install requirements
    pip install -r ./requirements.txt
    cd vrp
```
### brute force
```bash
    python core.py -s bruteforce
    # to see the execution details
    python core.py -s bruteforce -v
```

### alternative run
```bash
    python core.py --style <style> --filename <input filename (optional)> --verbose
    # or
    python core.py -s <style> -f <input filename (optional)> -v
```
## styles
* bruteforce
