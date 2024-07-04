# CAD-UWYO
### Code custom modifications
- create_geometry_3D = True/False (default = False) : Activates the simulation with thermal envelope from geometries
- calculate_volume_3D = True/False (default = False) : Activates the volume calculation from geometries
- citysim_filepath = r"---/CitySim.exe" : File path of the CitySim solver
- directory_path = r"---" : Name of the new directory to be created by the simulation
- climate_file = r"---.cli" : File path of the climate file
- horizon_file = r"---.hor" : File path of the horizon file

### Python libraries
The required libraries to import are listed in the *requirements.txt* file

### Results
The resulted .xml file in the 'output' folder along with summary results and generated plots.

## Bakcground
Olivier Chavanne established a framework to process and analyze information of all buildings in the area of study and simulate the surface temperature of those buildings through Citysim. To measure the heating demand of the University of Wyoming, Luke Macy needed to expand upon the framework to prepare additional logic, parameters, and assumptions for specialized simulations surrounding university infrastructure.
