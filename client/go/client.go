package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strings"
)

type Configuration struct {
	ServerUrl  string `json:"server_url"`
	ServerPort int    `json:"server_port"`
}

func LoadConfig(path string) Configuration {
	file, err := ioutil.ReadFile(path)

	if err != nil {
		log.Fatal("Config file missing: ", err)
	}
	var config Configuration

	err = json.Unmarshal(file, &config)

	if err != nil {
		log.Fatal("Config parse error: ", err)
	}

	return config
}

func main() {
	var (
		text string
	)

	configurationFile := flag.String("config", "~/.docit.json", "Configuration file. Default: ~/.docit.json")
	flagTag := flag.String("tags", "", "List of tags (comma separed)")
	flag.Parse()

	f, err := os.Stdin.Stat()
	if err != nil {
		log.Fatal("Stat() error", err)
	}

	if lText := flag.Args(); len(lText) != 0 {
		text = strings.Join(lText[:], " ")
	} else if (f.Size() > 0) || (f.Mode() & os.ModeNamedPipe != 0) {
		// TODO: eventually strip newlines
		bytes, err := ioutil.ReadAll(os.Stdin)
		if err != nil {
			log.Fatal("Cannot read from STDIN")
		}
		text = string(bytes)
	}  else {
		log.Fatal("You must specify some text")
	}

	config := LoadConfig(*configurationFile)
	tags := strings.Split(*flagTag, ",")

	fmt.Println(config.ServerUrl, tags, text)
}
