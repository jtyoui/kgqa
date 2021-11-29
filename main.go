// Package main
// @Time  : 2021/11/26 上午9:49
// @Author: Jtyoui@qq.com
package main

import (
	"embed"
	"encoding/csv"
	"fmt"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/golang-middleware/ginDist"
	"io"
	"net/http"
	"strings"
	"sync"
)

//go:embed web/dist
var fs embed.FS

//go:embed web/relation.csv
var dfs string

//go:embed web/questions.txt
var cfs string

var similar = strings.Split(cfs, "\n")

type Result struct {
	sync.Mutex
	Question string   `json:"-"`
	Data     []string `json:"data"`
	Code     int      `json:"code"`
	Sentence []string `json:"sentence"`
	Msg      string   `json:"msg"`
}

func unique(m []string) []string {
	d := make([]string, 0, len(m))
	tempMap := make(map[string]bool, len(m))
	for _, v := range m {
		if tempMap[v] == false {
			tempMap[v] = true
			d = append(d, v)
		}
	}
	return d
}

func (r *Result) getResult(wg *sync.WaitGroup) {
	defer wg.Done()
	cn := csv.NewReader(strings.NewReader(dfs))
	result := make([]string, 0, 10)
	for data, err := cn.Read(); err != io.EOF; data, err = cn.Read() {
		if err != nil || data[0] == "" || data[1] == "" || data[2] == "" {
			continue
		}
		var entity, relation, node = false, false, false
		if strings.Contains(r.Question, data[0]) {
			entity = true
		}
		if strings.Contains(r.Question, data[1]) {
			relation = true
		}
		if strings.Contains(r.Question, data[2]) {
			node = true
		}
		if entity && relation {
			result = append(result, data[2])
		} else if entity && node {
			result = append(result, data[1])
		} else if relation && node {
			result = append(result, data[0])
		}
	}

	result = unique(result)
	if len(result) == 0 {
		r.Code = 201
	}
	r.Data = result
}

func (r *Result) levenshteinDistance(s, t string, wg *sync.WaitGroup) {
	defer wg.Done()
	d := make([][]int, len(s)+1)
	for i := range d {
		d[i] = make([]int, len(t)+1)
	}
	for i := range d {
		d[i][0] = i
	}
	for j := range d[0] {
		d[0][j] = j
	}
	for j := 1; j <= len(t); j++ {
		for i := 1; i <= len(s); i++ {
			if s[i-1] == t[j-1] {
				d[i][j] = d[i-1][j-1]
			} else {
				min := d[i-1][j]
				if d[i][j-1] < min {
					min = d[i][j-1]
				}
				if d[i-1][j-1] < min {
					min = d[i-1][j-1]
				}
				d[i][j] = min + 1
			}
		}

	}
	flag := d[len(s)][len(t)]
	if flag < 10 && flag > 0 {
		r.Lock()
		if len(r.Sentence) < 5 {
			r.Sentence = append(r.Sentence, s)
		}
		r.Unlock()
	}
}

func (r *Result) compareString(wg *sync.WaitGroup) {
	defer wg.Done()
	cg := &sync.WaitGroup{}
	for _, value := range similar {
		cg.Add(1)
		go r.levenshteinDistance(value, r.Question, cg)
	}
	cg.Wait()
}

func Index(c *gin.Context) {
	question := c.Query("question")
	r := Result{Code: 200, Question: question}
	r.Sentence = make([]string, 0, 5)
	wg := &sync.WaitGroup{}
	wg.Add(2)
	go r.getResult(wg)
	go r.compareString(wg)
	wg.Wait()
	c.JSON(http.StatusOK, &r)
}

func main() {
	fmt.Println("😀开始启动中....")
	gin.SetMode(gin.ReleaseMode)
	router := gin.Default()
	_ = router.SetTrustedProxies([]string{"0.0.0.0"})
	router.Use(ginDist.Default(fs))
	router.Use(cors.Default())

	// 路由
	router.GET("/wss/qa", Index)
	fmt.Println("😁开始完毕！")
	// 启动
	fmt.Println("👉点击这里： http://localhost:16541/")
	if err := router.Run(":16541"); err != nil {
		panic("16541端口冲突")
	}
}
