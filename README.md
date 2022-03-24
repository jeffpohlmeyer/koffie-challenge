# Koffie Labs Frontend Challenge
## Installing Dependencies
### Python
After cloning the repo, create a python virtual environment and install the requirements
```bash
python -m venv env
source ./env/bin/activate # or .\env\Scripts\activate on Windows
pip install -r requirements.txt
```

## Running the app locally
Open a terminal, activate the virtual environment, navigate to the `koffie_frontend_challenge` sub-folder, and simply run the `usage.py` script
```bash
cd koffie_frontend_challenge
python ./usage.py
```
Then you should be able to open a browser window to http://localhost:8050

### Developing the React component
*Note:* You will need to have [Node.js](https://nodejs.org/en/) installed because there is a React component included in the project.  
Navigate to the `koffie_frontend_challenge directory` and install dependencies
```bash
cd ./koffie_frontend_challenge
npm i # or yarn install
```
You'll then want to open a second terminal window in the same location as this one.  
In one terminal you'll want to run
```bash
npx tailwindcss -i ./src/input.css -o ./assets/output.css --watch
```
and in the other terminal, any time you update the React component and need to re-build it, you'll have to run
```bash
npm run build
```
Then, in the window already focused on http://localhost:8050, you __may__ need to do a hard reload to clear the local cache to see the changes in your React component live.
