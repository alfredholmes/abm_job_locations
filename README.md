# Agent Based Model of UK Job Locations

This project models the movement of jobs around the UK's local authorities using an agent based approach.

The project uses ONS data for the initial configurations and calibration of the model as well as data for the positions of each local authority. See `data/sources.txt` for details

To Compile:
```
javac -cp src/ src/com/alfred/controller/Controller.java -d ./
```

And then to run:

```
java com.alfred.controller.Controller
```
