# LocalBrowser

LocalBrowser is a lightweight local application browser designed to run and display locally hosted applications using a simple URL scheme. It can also run as a standalone proxy server and provides options for cache control.

## Features

- Open local applications using a custom URL scheme
- Optional caching
- Built-in proxy server
- Example application for testing
- Simple command-line interface

## Installation

Install LocalBrowser using your preferred installation method.

## Usage

### Start LocalBrowser

```bash
localbrowser
```

### Disable Cache

Start LocalBrowser without using the cache:

```bash
localbrowser --no-cache
```

### Run Only the Proxy Server

Start only the built-in proxy server without opening the browser:

```bash
localbrowser --proxy
```

### Run the Example Application

Launch the included example application:

```bash
localbrowser --run-example
```

### Open an Application

Open a local application directly by providing its URL:

```bash
localbrowser <url>
```

Example:

```bash
localbrowser notes.john/
```

## URL Scheme

LocalBrowser uses the following URL format:

```
<identifier>/<path>
```

### Identifier

The identifier uniquely specifies an application and its owner:

```
<app_name>.<user>
```

Examples:

```
notes.john/
music.alice/library
todo.admin/tasks
```

### Path

The path specifies the resource inside the application.

Examples:

```
notes.john/
notes.john/settings
music.alice/playlists/favorites
```

## Command-Line Options

| Option | Description |
|---------|-------------|
| `--no-cache` | Disables the cache. |
| `--proxy` | Starts only the proxy server. |
| `--run-example` | Launches the included example application. |

## Examples

Start LocalBrowser normally:

```bash
localbrowser
```

Open an application:

```bash
localbrowser calculator.moritz/
```

Start without cache:

```bash
localbrowser --no-cache
```

Run only the proxy server:

```bash
localbrowser --proxy
```

Launch the example application:

```bash
localbrowser --run-example
```

## License

See the project's license file for licensing information.
