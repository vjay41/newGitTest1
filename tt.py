package main

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/lib/pq"
	dataframe "github.com/rocketlaunchr/dataframe-go"
)

var (
	host     = "localhost"
	port     = 5432
	user     = "your_postgres_user"
	password = "your_postgres_password"
	dbname   = "your_postgres_db"
)

// Function to query PostgreSQL and store the result in a dataframe
func queryToDataFrame(db *sql.DB, query string) (*dataframe.DataFrame, error) {
	// Execute the query
	rows, err := db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	// Get column names
	columns, err := rows.Columns()
	if err != nil {
		return nil, err
	}

	// Create a slice of interface to hold each row's values
	values := make([]interface{}, len(columns))
	for i := range values {
		values[i] = new(sql.RawBytes)
	}

	// Create a dataframe to store the results
	df := dataframe.New()

	// Read each row and add it to the dataframe
	for rows.Next() {
		err := rows.Scan(values...)
		if err != nil {
			return nil, err
		}

		// Convert SQL row values to a slice of interface{}
		row := make([]interface{}, len(values))
		for i, value := range values {
			row[i] = string(*value.(*sql.RawBytes)) // Convert RawBytes to string
		}

		// Append row to the dataframe
		df.Append(row)
	}

	return df, nil
}

func main() {
	// Build connection string for PostgreSQL
	psqlConnString := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		host, port, user, password, dbname)

	// Open a connection to the PostgreSQL database
	db, err := sql.Open("postgres", psqlConnString)
	if err != nil {
		log.Fatal("Error opening database connection: ", err)
	}
	defer db.Close()

	// Ping the database to verify connection
	err = db.Ping()
	if err != nil {
		log.Fatal("Error pinging database: ", err)
	}
	log.Println("Connected to PostgreSQL database!")

	// Define the query
	query := "SELECT * FROM your_table"

	// Query PostgreSQL and store the result in a dataframe
	df, err := queryToDataFrame(db, query)
	if err != nil {
		log.Fatal("Error querying PostgreSQL: ", err)
	}

	// Print the dataframe for validation
	fmt.Println(df.Table())
}
