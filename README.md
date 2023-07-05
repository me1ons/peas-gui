## Peas-GUI
对Peas的GUI实现。

### Prerequisites
`python2`  
`python3`  
`python setup.py install (这里是Peas的安装)`  

### Example usage

#### List file shares  
`python3 main.py -u admin -p admin --list-unc='\\Server01\' -ip 10.10.10.10`

#### Command line arguments
Run python3 peas-gui.py --help for the latest options.
```
usage: main.py [-h] -u U -p P --list-unc LIST_UNC -ip IP

options:
  -h, --help           show this help message and exit
  -u U                 Email User
  -p P                 Email Password
  --list-unc LIST_UNC  Unc List
  -ip IP               Download UncPath
```

### References and Acknowledgements
- https://github.com/WithSecureLabs/peas
