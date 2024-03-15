package main

import (
	"crypto/subtle"
	"embed"
	"fmt"
	"html/template"
	"net/http"
	"os"
	"path/filepath"

	"github.com/gin-gonic/gin"
	"github.com/jmoiron/sqlx"
	_ "github.com/mattn/go-sqlite3"
)

//go:embed views
var viewFS embed.FS

func must(err error) {
	if err != nil {
		fmt.Fprintln(os.Stderr, "Fatal error:", err)
		os.Exit(1)
	}
}

var flag string = os.Getenv("FLAG")

type Cents int

func (c Cents) String() string {
	return fmt.Sprintf("$%v.%02d", int(c)/100, int(c)%100)
}

type Listing struct {
	ID          string
	Title       string
	Description string
	PriceCents  Cents `db:"priceCents"`
	Image       string
}

type User struct {
	Username string
	Password string
}

func main() {
	db := sqlx.MustOpen("sqlite3", "file:db.sqlite3")

	e := gin.Default()
	e.SetHTMLTemplate(template.Must(template.ParseFS(viewFS, "views/**")))

	e.GET("/", func(c *gin.Context) {
		listings := make([]Listing, 0)
		err := db.Select(&listings, "SELECT * FROM listing;")
		if err != nil {
			c.AbortWithError(http.StatusInternalServerError, err)
			return
		}
		c.HTML(http.StatusOK, "index.html", gin.H{"Listings": listings})
	})
	e.GET("/search", func(c *gin.Context) {
		query := c.Query("q")
		listings := make([]Listing, 0)
		err := db.Select(&listings, `
			SELECT *
			FROM listing
			WHERE title LIKE '%' || ? || '%'
			OR description LIKE '%' || ? || '%';
		`, query, query)
		if err != nil {
			c.AbortWithError(http.StatusInternalServerError, err)
			return
		}
		c.HTML(http.StatusOK, "search.html", gin.H{
			"Listings": listings,
			"Query":    query,
		})
	})
	e.GET("/product", func(c *gin.Context) {
		id := c.Query("id")
		var listing Listing
		err := db.Get(&listing, "SELECT * from listing WHERE id = ?;", id)
		if err != nil {
			c.AbortWithError(404, err)
			return
		}
		c.HTML(http.StatusOK, "product.html", listing)
	})
	e.GET("/assets", func(c *gin.Context) {
		id := c.Query("id")
		path := filepath.Join("assets", filepath.Clean(id))
		c.File(path)
	})
	e.GET("/cart", underConstruction)
	e.GET("/admin", func(c *gin.Context) {
		cookie, err := c.Cookie("FLAG")
		if err != nil || subtle.ConstantTimeCompare([]byte(cookie), []byte(flag)) == 0 {
			c.HTML(http.StatusOK, "admin.html", nil)
			return
		}
		c.String(http.StatusOK, flag)
	})
	e.POST("/admin", func(c *gin.Context) {
		username := c.PostForm("username")
		password := c.PostForm("password")
		var user User
		err := db.Get(&user, "SELECT * FROM user WHERE username = ?", username)
		if err != nil {
			c.HTML(http.StatusUnauthorized, "admin.html", "Username or password is incorrect")
			return
		}
		if subtle.ConstantTimeCompare([]byte(password), []byte(user.Password)) == 0 {
			c.HTML(http.StatusUnauthorized, "admin.html", "Username or password is incorrect")
			return
		}
		c.Writer.Header().Add("Set-Cookie", "FLAG="+flag)
		c.Writer.Header().Add("Content-Type", "text/plain")
		c.Writer.WriteString(flag)
	})

	if os.Getenv("LIVE_RELOAD") != "" {
		e.Use(func(c *gin.Context) {
			e.LoadHTMLGlob("views/**")
		})
	}

	must(e.Run("0.0.0.0:8080"))
}

func underConstruction(c *gin.Context) {
	c.HTML(http.StatusOK, "under-construction.html", gin.H{"BackURL": c.Request.Referer()})
}
