# oscpygpio

Control the GPIO pins of a RPI (Raspbery PI) with OSC commands
You could use any OSC source device but this is designed to work with the great [companion](https://bitfocus.io/companion) software.

There is a wrapper script to run the actual Python code although this is not really finished

the Python code also has #* comments noting places that need further work...

However it is verison 1.0!

## conf file layout

```JSON
{
    "pins": {
        "12": {
            "HIGH": [
                { "path": "/style/text/1/6", "value": "12 HIGH" },
                { "path": "/style/bgcolor/1/6", "value": [20,20,20] }
            ],
            "LOW": [
                { "path": "/style/text/1/6", "value": "12 LOW" },
                { "path": "/style/bgcolor/1/6", "value": [120,120,120] }
            ]
        }
    }
}
```

The first thing to fix is JIT loading responses in the read_gpio function from the config file!

Credit to for the OSC libary:
https://python-osc.readthedocs.io/
