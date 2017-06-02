package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
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
	configurationFile := flag.String("config", "~/.docit.json", "Configuration file. Default: ~/.docit.json")
	flag.Parse()
	config := LoadConfig(*configurationFile)
	fmt.Println(config.ServerUrl)
	fmt.Println(config.ServerPort)
}
