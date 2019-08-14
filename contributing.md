# Contribution guide

The "lmao-bot" repository contains a solution that holds both the code that runs lmao-bot on Discord, as well as a class library for storing common database objects used in other lmao projects, such as a web interface. It also contains a web api which acts as a middleman between the bot and the database for enhanced security and the potential for additional features in the future.

If you're interested in contributing to this project, great! This file should help you get started.

## Types of contribution

There are many ways you can help improve this repository! For example:

-   **Create a brand-new feature:** maybe you want some sort of "ban everyone" command?
-   **Fix a bug:** we have a list of [issues](https://github.com/DrEngi/lmao-bot/issues),
    or maybe you found your own.


## Setup

To contribute and test, you'll need Visual Studio 2019 (or, if you want, you can use any code editor such as VS Code or Atom with the dotnet CLI.) You'll also need a github account (and git!) to get the code. If you're interested in working on music, you'll also need to install Java to run [Lavalink](https://github.com/Frederikam/Lavalink).

Please ensure the the [dotnet sdk](https://dotnet.microsoft.com/download) is installed on your machine. Visual Studio 2019 users can install this by choosing the .NET Core Workflow in the Visual Studio Installer. *Note: .NET Core 3.0 is required.*

lmao-bot has changed from using JSON files to [MongoDB](https://www.mongodb.com/) for data storage. This means you'll need to setup your own local mongo instance to talk to lmao-bot. Please see this [installation tutorial](https://docs.mongodb.com/manual/administration/install-community/) for help on installing MongoDB on your machine.

As far as text/code editors go, there are more editors than you can shake a stick at, so it's down to personal preference. [Atom](https://atom.io/) is a great, open source editor we can definitely recommend (and one of us uses it).

For more information on setting up Git on your machine, [read this article](https://help.github.com/articles/set-up-git/).

With the above dependencies satisfied, [create your new account on Github](https://github.com/join).

### Fork and clone

Next up, you need to fork and clone the repo to be able to contribute to it. You can [learn about forking on Github](https://help.github.com/articles/fork-a-repo). Once you have your own fork, [clone it to your local machine](https://help.github.com/articles/cloning-a-repository/).

Finally, change into the new directory created by the clone and open the lmao-bot solution and start working. The main bot rests within the lmao-bot project. If you're looking to change the database schemas (by editing anything in `lmaocore`), you may do so, but please provide explicit reasoning in your pull request as well as methods for converting current objects into your new versions.

### Testing

To test the bot, you'll need to create a config.json and place it within the root directory of your build folder (usually lmao-bot/lmao-bot/bin/Debug/netcoreapp2.2 or similar.). This configuration file will contain your bot token and Mongo connection information. If you're you're using lavalink, that information will go here as well. To get a bot token, create an account on the discord developer portal and create a bot user.

I'm updating the project structure to abstract away the database access from the actual bot. While this may feel like a step backwards at first, it's so that the bot can have multiple fall-backs if the database crashes, and allows me to create other projects that connect to it. There are two configurations you need, one for the bot and another for the API.

Bot config:
```json
{
  "Token": "token",
  "Dbl": null,
  "Api": {
    "URL": "http://your.lmao.site",
    "Port": 8080,
    "AuthKey": "yourverysecureauthkeyforlmaohere"
  },
  "Mongo": {
    "Hostname": "127.0.0.1",
    "Port": 27017,
    "User": "user",
    "Password": "password",
    "Database": "lmao"
  },
  "Lavalink": {
    "Hostname": "127.0.0.1",
    "Port": 2333,
    "Region": "us",
    "Password": "exampleverylongandverysecurelavalinkpasshere",
    "Name": "default-node"
  }
}
```

API config:
```json
{
  "lmaoauthkey": "yourverysecureauthkeyforlmaohere",
  "Lavalink": {
    "Hostname": "127.0.0.1",
    "Port": 2333,
    "Region": "us",
    "Password": "exampleverylongandverysecurelavalinkpasshere",
    "Name": "default-node"
  },
  "Mongo": {
    "Hostname": "127.0.0.1",
    "Port": 27017,
    "User": "user",
    "Password": "password",
    "Database": "lmao"
  },
}
```

Fill in all data as you like. The DBL field is used for the token that belongs to the public version of lmao-bot, you can leave this as null and DBL won't be initialized. If you're using lavalink, specify the connection information for your Lavalink instance. If you're not using it, setting the object to null will cause music and playlists to not be initialized.

### Pull Requests

Once you're satisfied, [submit your pull request](https://help.github.com/articles/creating-a-pull-request/). Please be sure you create a pull request to the REWRITE branch, not to master or develop (this is for the python version right now). Direct PRs to master/develop will be denied as they skip crucial build checks and ruin my OCD.

## Thank you!

Thank you for your contribution ~ o/\o
