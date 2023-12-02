# File Structure
### `Utility_Disconnection_Dashboard_App/`
This is the base directory of the application
- `app.py` - the main application  
- `config.py` - settings for the application  
- `assets/` - images, icons, thumbnails for the application  
- `stylesheets/` - css styles  

### `Utility_Disconnection_Dashboard_App/disconnection_policies/`
This is a package for Disconnection Policies
- `visualization.py` - plotly graphs for visualization
- `utils.py` - helper functions for downloading data  
- `config.py` - settings for `visualization.py` and `utils.py`  
- `assets/` - images, icons, thumbnails for generating excels, currently unused  
- `data/` - data used

### `Utility_Disconnection_Dashboard_App/utility_disconnections/`
This is a package for Utility Disconnections
- `visualization.py` - plotly graphs for visualization 
- `utils.py` - helper functions for downloading data  
- `config.py` - settings for `visualization.py` and `utils.py` 
- `assets/` - images, icons, thumbnails for generating excels, currently unused  
- `data/` - data used