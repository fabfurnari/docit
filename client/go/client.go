package main

import (
	"fmt"
	"io/ioutil"
	"os/user"
	"path/filepath"
	"runtime"
)

type config struct{
	ServerUrl   string
	ServerToken string
}

var flagVersion bool
var version = "0.1"

func init() {
	read_configurations()
}

func config_files() []string {
	// list possible configuration files
	config_files := []string{}

	if runtime.GOOS == "linux" {
		config_files = append(config_files, "/etc/docit.conf")
	}

	usr, err := user.Current()
	if err == nil {
		config_files = append(config_files, filepath.Join(usr.HomeDir, ".docit.conf"))
	}

	config_files = append(config_files, ".docit.conf")

	return config_files
}

func read_configurations() {
	config_files := config_files()

	for _, file := range config_files {
		err := read_configuration(file)
	}
}

func read_configuration(filename string) error {
	data, error := ioutil.ReadFile(filename)
	if error != nil {
		return nil
	}

}
