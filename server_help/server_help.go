package server_help

import (
	"embed"
	"strings"
)

//go:embed statement_*.txt
var help_docs embed.FS

type HelpDoc struct {
	Name        string
	Description string
	Example     string
}

func HelpForTopic(topic string) (*HelpDoc, error) {
	topic = strings.ToLower(topic)
	helpText, err := help_docs.ReadFile("statement_" + topic + ".txt")
	if err != nil {
		return nil, err
	}
	return &HelpDoc{topic, string(helpText), ""}, nil
}
