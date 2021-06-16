package server_help

import "testing"

func TestServerHelpSelect(t *testing.T) {
	_, err := HelpForTopic("select")
	if err != nil {
		t.Errorf("error for select is not nil")
	}
}

func TestServerHelpNonexistend(t *testing.T) {
	_, err := HelpForTopic("nonexistend")
	if err == nil {
		t.Errorf("error for nonexistend is nil")
	}
}
