# OpenABIS Secugen: Python binding for SecuGen SDK

This is a Python/CFFI binding for the SecuGen SDK specialized in minutiae manipulation.

It works on Windows i386/x64 and on Linux i386/x64 (only tested on Red Hat 6).

The bundled SecuGen libraries were copied from the following SDKs:

 - FDx SDK Pro for Linux v3.71c 2
 - FDx SDK Pro for Windows v3.7_J14


## Installation

**Pipenv**
```
pipenv install git+https://github.com/openabis/openabis-secugen.git@master#openabis_secugen
```

**Pip**
```
pip install git+https://github.com/openabis/openabis-secugen.git@master
```

## Usage
`SecuGen` accepts `config` as parameter. 

Path to the libraries is a requirement and should be provied in the `config`:
```text
LIBSGFDU03 (str) - path to filename `libsgfdu03.so`
LIBSGFPAMX (str) - path to filename `libsgfpamx.so`
LIBSGFPLIB (str) - path to filename `libsgfplib.so`
SGFPLIB (str) - path to filename `sgfplib`
```

Configurations needed for the process:

```text
SECUGEN_MATCH_SECURITY_LEVEL (int) - security level defined by the app, default is 5
```
