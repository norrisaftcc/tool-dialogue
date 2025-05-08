# tool-dialogue

intended as a basic twine alternative that didn't require any external tools. Just load the json and play. Editor as a separate program.

the 80s terminal aesthetic is to evoke a time when carefully staring at a menu before clicking was high gameplay.

# Running the tool (part 1 -- venv stuff)

I see you're now in your project directory and tried to create a virtual environment but got the usage instructions instead. Let's pick up from here and set up both Streamlit and Node.js properly.

## Setting up a Streamlit Environment

First, let's create a virtual environment for your Streamlit projects:

```
python -m venv streamlit_env
```

This will create a directory called `streamlit_env` in your current location with a self-contained Python environment.

To activate this environment:

```
source streamlit_env/bin/activate
```

You should see `(streamlit_env)` at the beginning of your command prompt, indicating that the environment is active.

Now, let's install Streamlit:

```
pip install streamlit
```

To test your Streamlit installation:

```
streamlit hello
```

This should open a demo app in your browser.

## Setting up Node.js

Let's install Node.js with Homebrew:

```
brew install node
```

Verify your Node.js installation:

```
node --version
npm --version
```

Now you have both Streamlit and Node.js properly installed, with Streamlit in a dedicated virtual environment that won't conflict with other Python projects.

## venv tldr
Setting up a Streamlit Environment
First, let's create a virtual environment for your Streamlit projects:
python -m venv streamlit_env
This will create a directory called streamlit_env in your current location with a self-contained Python environment.
To activate this environment:
source streamlit_env/bin/activate
You should see (streamlit_env) at the beginning of your command prompt, indicating that the environment is active.
Now, let's install Streamlit:
pip install streamlit
To test your Streamlit installation:
streamlit hello
This should open a demo app in your browser.
Setting up Node.js
Let's install Node.js with Homebrew:
brew install node
Verify your Node.js installation:
node --version
npm --version
Now you have both Streamlit and Node.js properly installed, with Streamlit in a dedicated virtual environment that won't conflict with other Python projects.

----


