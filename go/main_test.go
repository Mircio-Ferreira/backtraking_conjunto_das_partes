package main

import (
	"bytes"
	"os"
	"path/filepath"
	"reflect"
	"regexp"
	"strconv"
	"strings"
	"testing"
)

func TestIntegrationBenchmarkFlow(t *testing.T) {
	alphabet := generateAlphabet(3)
	if got, want := string(alphabet), "ABC"; got != want {
		t.Fatalf("alphabet mismatch: got %q want %q", got, want)
	}

	var subsets []string
	backtrack(alphabet, 0, len(alphabet), nil, func(current []byte) {
		subsets = append(subsets, string(current))
	})

	wantSubsets := []string{"ABC", "AB", "AC", "A", "BC", "B", "C", ""}
	if !reflect.DeepEqual(subsets, wantSubsets) {
		t.Fatalf("subsets mismatch:\n got %#v\nwant %#v", subsets, wantSubsets)
	}

	dir := t.TempDir()
	smallFile := filepath.Join(dir, "SMALL_TEST")
	middleFile := filepath.Join(dir, "MIDDLE_TEST")
	bigFile := filepath.Join(dir, "BIG_TEST")

	for _, file := range []string{smallFile, middleFile, bigFile} {
		if err := os.WriteFile(file, []byte("stale data\n"), 0644); err != nil {
			t.Fatal(err)
		}
	}

	cfg := benchmarkConfig{
		bigSetSize: 3,
		runs:       2,
		eraseFiles: true,
		cases: []benchmarkCase{
			{setSize: 1, outputFile: smallFile, doneMessage: "end small test"},
			{setSize: 2, outputFile: middleFile, doneMessage: "end middle test"},
			{setSize: 3, outputFile: bigFile, doneMessage: "end big test"},
		},
	}

	var output bytes.Buffer
	runBenchmarks(&output, cfg)

	if got, want := output.String(), "test star\nend small test\nend middle test\nend big test\n"; got != want {
		t.Fatalf("stdout mismatch:\n got %q\nwant %q", got, want)
	}

	assertBenchmarkFile(t, smallFile, 1, 2)
	assertBenchmarkFile(t, middleFile, 2, 2)
	assertBenchmarkFile(t, bigFile, 3, 2)

	exactFile := filepath.Join(dir, "exact.txt")
	writeResult(exactFile, 4, 1.23456789)

	data, err := os.ReadFile(exactFile)
	if err != nil {
		t.Fatal(err)
	}
	if got, want := string(data), "len set 4 time: 1.234567890\n"; got != want {
		t.Fatalf("exact write mismatch: got %q want %q", got, want)
	}

	truncateTestFile(exactFile)
	data, err = os.ReadFile(exactFile)
	if err != nil {
		t.Fatal(err)
	}
	if len(data) != 0 {
		t.Fatalf("truncate failed: got %q", string(data))
	}
}

func assertBenchmarkFile(t *testing.T, file string, setSize, wantLines int) {
	t.Helper()

	data, err := os.ReadFile(file)
	if err != nil {
		t.Fatal(err)
	}
	if strings.Contains(string(data), "stale") {
		t.Fatalf("file was not truncated before benchmark: %q", string(data))
	}

	lines := strings.Split(strings.TrimSpace(string(data)), "\n")
	if len(lines) != wantLines {
		t.Fatalf("line count mismatch for %s: got %d want %d", file, len(lines), wantLines)
	}

	pattern := regexp.MustCompile(`^len set ` + regexp.QuoteMeta(strconv.Itoa(setSize)) + ` time: \d+\.\d{9}$`)
	for _, line := range lines {
		if !pattern.MatchString(line) {
			t.Fatalf("bad benchmark line for %s: %q", file, line)
		}
	}
}
