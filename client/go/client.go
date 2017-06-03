package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
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

func PerformRequest(url string, text string) (statusCode string, err error) {
	log.Printf("Performing request %s to %s", text, url)
	req, err := http.NewRequest("POST", url, bytes.NewBufferString(text))
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		log.Println("Error while performing request: ", err)
		return "", err
	}
	defer resp.Body.Close()
	log.Println("Response headers: ", resp.Header)
	log.Println("Response code: ", resp.Status)
	return resp.Status, nil
	
}

func main() {
	var (
		text string
	)
	configFlag := flag.String("config", "", "Configuration file. Default: ~/.docit.json")
	flagTag := flag.String("tags", "", "List of tags (comma separed)")
	flagVerbose := flag.Bool("v", false, "Turn on verbose logging")
	flag.Parse()

	if !*flagVerbose {
		log.SetOutput(ioutil.Discard)
	}

	f, err := os.Stdin.Stat()
	if err != nil {
		log.Fatal("Stat() error", err)
	}

	if lText := flag.Args(); len(lText) != 0 {
		text = strings.Join(lText[:], " ")
	} else if (f.Size() > 0) || (f.Mode()&os.ModeNamedPipe != 0) {
		// TODO: eventually strip newlines
		bytes, err := ioutil.ReadAll(os.Stdin)
		if err != nil {
			log.Fatal("Cannot read from STDIN")
		}
		text = string(bytes)
	} else {
		log.Fatal("You must specify some text")
	}

	configFile, err := GetConfigurationFile(configFlag)
	if err != nil {
		log.Fatal("Cannot get configuration!")
	}
	log.Println("Using configuration file: ", configFile)
	config := LoadConfig(configFile)
	tags := strings.Split(*flagTag, ",")

	log.Println(config.ServerUrl, tags, text)
	code, _ := PerformRequest(config.ServerUrl, text)
	fmt.Println(code)
}
