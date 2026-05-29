package main

import (
	"container/list"
	"fmt"
	"io"
	"os"
	"syscall"
)

const (
	smallSetSize  = 20
	middleSetSize = 25
	bigSetSize    = 30
	testRuns      = 5

	eraseTestFiles = true

	smallOutputFile  = "go/case_tests_go/SMALL_TEST"
	middleOutputFile = "go/case_tests_go/MIDDLE_TEST"
	bigOutputFile    = "go/case_tests_go/BIG_TEST"
)

type benchmarkCase struct {
	setSize     int
	outputFile  string
	doneMessage string
}

type benchmarkConfig struct {
	bigSetSize int
	runs       int
	eraseFiles bool
	cases      []benchmarkCase
}

func main() {
	runBenchmarks(os.Stdout, defaultBenchmarkConfig())
}

func defaultBenchmarkConfig() benchmarkConfig {
	return benchmarkConfig{
		bigSetSize: bigSetSize,
		runs:       testRuns,
		eraseFiles: eraseTestFiles,
		cases: []benchmarkCase{
			{setSize: smallSetSize, outputFile: smallOutputFile, doneMessage: "end small test"},
			{setSize: middleSetSize, outputFile: middleOutputFile, doneMessage: "end middle test"},
			{setSize: bigSetSize, outputFile: bigOutputFile, doneMessage: "end big test"},
		},
	}
}

func runBenchmarks(output io.Writer, cfg benchmarkConfig) {
	alphabet := generateAlphabet(cfg.bigSetSize)

	if !validBenchmarkConfig(cfg) {
		fmt.Fprint(output, "ERRO: BIG CASES NEED TO BE BIGGER THAN MIDDLE OR SMALL")
		return
	}

	if cfg.eraseFiles {
		for _, benchmark := range cfg.cases {
			truncateTestFile(benchmark.outputFile)
		}
	}

	fmt.Fprintln(output, "test star")

	for _, benchmark := range cfg.cases {
		for i := 0; i < cfg.runs; i++ {
			runBenchmark(benchmark.setSize, alphabet, benchmark.outputFile)
		}

		fmt.Fprintln(output, benchmark.doneMessage)
	}
}

func validBenchmarkConfig(cfg benchmarkConfig) bool {
	for _, benchmark := range cfg.cases {
		if cfg.bigSetSize < benchmark.setSize {
			return false
		}
	}

	return true
}

func generateAlphabet(n int) []byte {
	alphabet := make([]byte, n)
	for i := range alphabet {
		alphabet[i] = byte('A' + i)
	}
	return alphabet
}

func backtrack(alphabet []byte, idx, n int, current *list.List, visit func([]byte)) {
	if current == nil {
		current = list.New()
	}

	if idx == n {
		if visit != nil {
			visit(listBytes(current))
		}
		return
	}

	current.PushBack(alphabet[idx])
	backtrack(alphabet, idx+1, n, current, visit)
	current.Remove(current.Back())
	backtrack(alphabet, idx+1, n, current, visit)
}

func listBytes(current *list.List) []byte {
	result := make([]byte, 0, current.Len())
	for e := current.Front(); e != nil; e = e.Next() {
		result = append(result, e.Value.(byte))
	}
	return result
}

func runBenchmark(setSize int, alphabet []byte, fileName string) {
	start := processCPUSeconds()
	backtrack(alphabet, 0, setSize, nil, nil)
	writeResult(fileName, setSize, processCPUSeconds()-start)
}

func processCPUSeconds() float64 {
	var usage syscall.Rusage
	if err := syscall.Getrusage(syscall.RUSAGE_SELF, &usage); err != nil {
		return 0
	}

	return float64(usage.Utime.Sec+usage.Stime.Sec) +
		float64(usage.Utime.Usec+usage.Stime.Usec)/1_000_000
}

func writeResult(filename string, setSize int, seconds float64) {
	file, err := os.OpenFile(filename, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
	if err != nil {
		fmt.Println("Erro ao abrir arquivo")
		return
	}
	defer file.Close()

	fmt.Fprintf(file, "len set %d time: %.9f\n", setSize, seconds)
}

func truncateTestFile(filename string) {
	file, err := os.OpenFile(filename, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0644)
	if err != nil {
		fmt.Println("Erro ao abrir arquivo")
		return
	}
	file.Close()
}
