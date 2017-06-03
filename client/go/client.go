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

func GetDefaultConfigFile() (string, error) {
	// Currently error not populated
	// maybe in the future
	defaultConfigFile := fmt.Sprintf("%s/%s", os.Getenv("HOME"), ".docit.json")
	return defaultConfigFile, nil
}

func GetConfigurationFile(configFlag *string) (string, error) {
	// Set configuration file order
	if *configFlag != "" {
		log.Println("Using flag for config file: ", *configFlag)
		return *configFlag, nil
	} else if envConf := os.Getenv("DOCIT_CONF"); envConf != "" {
		log.Println("Using envvar for config file")
		return envConf, nil
	} else {
		log.Println("Using default config file")
		c, err := GetDefaultConfigFile()
		if err != nil {
			return "", err
		}
		return c, nil
	}
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
	configFlag := flag.String("config", "", "Configuration file. Default: ~/.docit.json")
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

	configFile, err := GetConfigurationFile(configFlag)
	if err != nil {
		log.Fatal("Cannot get configuration!")
	}
	log.Println("Using configuration file: ", configFile)
	config := LoadConfig(configFile)
	tags := strings.Split(*flagTag, ",")

	fmt.Println(config.ServerUrl, tags, text)
}
