USE marketing_db;


-- ******************************** dim PRODUCT TABLE ********************************--
SELECT * FROM products;

SELECT 
	ProductID,
    ProductName,
    Price,
    CASE
		WHEN Price < 50 THEN "Low"
        WHEN Price BETWEEN 50 AND 100 THEN "Medium"
        ELSE "High"
	END AS PriceCategory
FROM products;


-- ******************************** dim CUSTOMER TABLE ********************************--
SELECT * FROM geography;
SELECT * FROM customers;

SELECT 
	c.CustomerID,
    c.CustomerName,
    c.Email,
    c.Gender,
    c.Age,
    g.Country,
    g.City 
FROM customers c
LEFT JOIN geography g
ON c.GeographyID = g.GeographyID;

-- ******************************** fact CUSTOMER_REVIEWS TABLE ********************************--

SELECT * FROM customer_reviews;

SELECT
	ReviewID,
    CustomerID,
    ProductID,
	ReviewDate,
    Rating, 
    REPLACE(ReviewText, "  "," ") AS "ReviewText"
FROM customer_reviews;


-- ******************************** fact ENGAGEMENT DATA TABLE ********************************--
SELECT * FROM engagement_data;

SELECT
    EngagementID,
    ContentID,
    CampaignID,
    ProductID,
    UPPER(REPLACE(ContentType, 'SOCIALMEDIA', 'Social Media')) AS ContentType,
     EngagementDate,
    -- DATE_FORMAT(STR_TO_DATE(EngagementDate, '%Y-%m-%d'), '%d.%m.%Y') AS EngagementDate
    LEFT(ViewsClicksCombined, LOCATE('-', ViewsClicksCombined) - 1) AS Views,
    SUBSTRING(ViewsClicksCombined, LOCATE('-', ViewsClicksCombined) + 1) AS Clicks,
	Likes
FROM engagement_data
WHERE ContentType != 'Newspaper';


-- ******************************** fact CUSTOMER JOURNEY TABLE ********************************--
SELECT * FROM customer_journey;

WITH DuplicateRecords AS (
SELECT
	JourneyID,
	CustomerID,
	ProductID,
	VisitDate,
	Stage,
	Action,
	Duration,
	ROW_NUMBER() OVER(PARTITION BY CustomerID, ProductID, VisitDate, Stage, Action
	ORDER BY JourneyID) AS row_num
	FROM customer_journey
	)
	SELECT * FROM DuplicateRecords
	WHERE row_num > 1
	ORDER BY JourneyID;
    
    -- Put avg_duration values where Duration column has NULL values --
SELECT
	JourneyID,
	CustomerID,
	ProductID,
    VisitDate,
	Stage,
	Action,
	ROUND(COALESCE(Duration, avg_duration),0) AS Duration
FROM
	(
		SELECT
			JourneyID,
			CustomerID,
			ProductID,
			VisitDate,
			UPPER(Stage) AS Stage,
			Action,
			Duration,
			AVG(Duration) OVER(PARTITION BY VisitDate) AS avg_duration,
			ROW_NUMBER() OVER(PARTITION BY CustomerID, ProductID, VisitDate, UPPER(Stage), Action ORDER BY JourneyID) AS row_num
		FROM customer_journey) AS SubQuery
		WHERE row_num = 1;












































































