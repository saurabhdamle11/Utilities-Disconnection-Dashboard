# Summary of app.py
## This is an overview of each region in app.py
## Please try to maintain the structure of app.py with regions
### Navigation Bar
- Navigation Bar Components - `nav_bar` contains the main dropdown that toggles between two modes: `Disconnection Policies` and `Utility Disconnections`.  
### Content
- Placeholder Components for `content` - `content` is the central part of the page. It is devided into four parts: map (top left), text below map (bottom left), filter (top right), mini graph (top right). They are empty placeholders that will be populated later.
- Injection Callbacks for `content` - Depending on the mode selected in the main dropdown, different component are injected into each of the four content placeholders.
- `content` Components Update Callbacks - The injected components are updated here. Graphs are retrieved through helper functions from `disconnection_policies/visualiation.py` and `utility_disconnections/visualiation.py`.  
### About Us Bar
- About Us Bar Components - `about_us` is the bar on the bottom of the page, containing a button for downloading data. Similar to `content`, there is an empty placeholder for the download button.  
Why don't we use a single download button? This is to decouple the download logic for the two mode, preventing large and complexe callbacks for downloading data.  
- Injection Callbacks for `about_us` - Depending on the mode selected in the main dropdown, button with the corresponding id is injected into the `about_us` bar.
### Welcome Modal
- Modal Components - the welcome message displayed when first entering the site.
- Modal Callback - a simple callback to close the modal with the close button
