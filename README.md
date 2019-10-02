# OpenAbis/Secugen: Python binding for SecuGen SDK

This is a Python/CFFI binding for the SecuGen SDK specialized in minutiae manipulation.

It works on Windows i386/x64 and on Linux i386/x64 (only tested on Red Hat 6).

The bundled SecuGen libraries were copied from the following SDKs:

 - FDx SDK Pro for Linux v3.71c 2
 - FDx SDK Pro for Windows v3.7_J14


_**Important**_

_SDKs should be stored in `lib/` directory inside the project working directory._

_The following is an example._

```
--project root
    ---lib/
        --- secugen/
            --- windows/
                ---- i386/
                ---- 64/
            ---- linux/
                ---- i386/
                ---- 64/

```

**Installation**

Pipenv

```
pipenv install -e git+https://github.com/newlogic42/openabis-secugen.git@master#openabis_secugen
```
