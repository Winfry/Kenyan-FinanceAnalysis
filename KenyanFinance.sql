SELECT * FROM [dbo].[IBRD_Loans_to_Kenya]
SELECT * FROM [dbo].[IDA_Credits___Grants_to_Kenya]
SELECT * FROM [dbo].[IFC_Investment_Projects_in_Kenya]

-----The Projects that were Granted Loans -------
SELECT Borrower, Guarantor, Project_Name
FROM [dbo].[IBRD_Loans_to_Kenya]
GROUP BY Borrower, Guarantor, Project_Name;

-------Projects that got Access to Credits ------
SELECT Borrower, Project_Name
FROM [dbo].[IDA_Credits___Grants_to_Kenya]
GROUP BY Borrower, Project_Name;

--------The Financial nstitutions which were inevsted on ----------- 
SELECT Company_Name, Industry, Project_Name, Document_Type
FROM  [dbo].[IFC_Investment_Projects_in_Kenya]
WHERE Industry = 'Financial Institutions'

------The Projects which were granted Credits and Took action and credits were fully paid Back-----
SELECT Project_Name , Disbursed_Amount, Agreement_Signing_Date
FROM [dbo].[IDA_Credits___Grants_to_Kenya]
WHERE Credit_Status = 'Fully Repaid'
ORDER BY Disbursed_Amount ASC;

------To calculate and find the total amount of loans the Kenyan Instititions has and the projects these loans went to which are fully repaid------
SELECT COUNT(DISTINCT Borrower) AS Total_Borrower, Borrower, Guarantor, Project_Name
FROM [dbo].[IBRD_Loans_to_Kenya]
WHERE Guarantor = 'Kenya'
    AND Loan_Status = 'Fully Repaid'
GROUP BY Borrower, Guarantor, Project_Name;    

------Projects that use the highest amounts of money that was loaned to Kenya ----
SELECT Borrower, Guarantor, Project_Name, Disbursed_Amount, Interest_Rate
FROM [dbo].[IBRD_Loans_to_Kenya]
WHERE Loan_Status = 'Fully Repaid'
GROUP BY Borrower, Guarantor, Project_Name, Disbursed_Amount , Interest_Rate
ORDER BY Disbursed_Amount DESC;

-------Checking the dates of the complete payments of the most expensive credits ------
SELECT Borrower, Project_Name, Disbursed_Amount,Board_Approval_Date ,Last_Repayment_Date
FROM[dbo].[IDA_Credits___Grants_to_Kenya]
WHERE Due_to_IDA =0 
    AND Credit_Status = 'Fully Repaid'
GROUP BY Borrower, Project_Name, Disbursed_Amount,Board_Approval_Date ,Last_Repayment_Date
ORDER BY Disbursed_Amount DESC;

-------The Industry that has the highest Investments which were approvved by the Board are very active ----
SELECT Industry, Company_Name, Project_Name, Total_IFC_investment_as_approved_by_Board_Million_USD
FROM[dbo].[IFC_Investment_Projects_in_Kenya]  
WHERE Status = 'Active'
    AND Total_IFC_investment_as_approved_by_Board_Million_USD > 50
ORDER BY Total_IFC_investment_as_approved_by_Board_Million_USD DESC   

--------Joining queries to find similar Borrowers of Kenya that have beeen Fully repaid----
SELECT *
FROM [dbo].[IBRD_Loans_to_Kenya] 
JOIN [dbo].[IDA_Credits___Grants_to_Kenya]
ON [dbo].[IBRD_Loans_to_Kenya].[Borrower] = [dbo].[IDA_Credits___Grants_to_Kenya].[Borrower]
WHERE Guarantor = 'Kenya'
  AND Loan_Status = 'Fully Repaid'

------To find out the similar projects that have been worked on by loans and the ones invested in ------
 SELECT *
FROM [dbo].[IFC_Investment_Projects_in_Kenya]
INNER JOIN [dbo].[IBRD_Loans_to_Kenya]
ON [dbo].[IFC_Investment_Projects_in_Kenya].[Project_Name] = [dbo].[IBRD_Loans_to_Kenya].[Project_Name]
WHERE Status = 'Fully Repaid' 

----------Joining Project IDs that have the same ID in loans and have been invested in ----------- 
SELECT Project_ID
FROM [dbo].[IBRD_Loans_to_Kenya]
LEFT JOIN [dbo].[IFC_Investment_Projects_in_Kenya]
ON [dbo].[IFC_Investment_Projects_in_Kenya].[Industry] = [dbo].[IBRD_Loans_to_Kenya].[Project_Name]

-------------Specific Cancelled Loaned Projects With high Interest Rates------
SELECT count(DISTINCT Borrower) AS Borrower_Number, Guarantor, Project_Name, Project_ID
FROM [dbo].[IBRD_Loans_to_Kenya]
WHERE Interest_Rate > 5.0
   AND Loan_Status = 'Fully Cancelled'
GROUP BY Borrower, Guarantor ,Project_Name,Project_ID

-------------Specific Cancelled Credited Projects that have a high service change rate ------
SELECT count(DISTINCT Borrower) AS Borrower_Number, Project_Name, Project_ID, Cancelled_Amount,Service_Charge_Rate
FROM [dbo].[IDA_Credits___Grants_to_Kenya]
WHERE Service_Charge_Rate > 0.5
   AND Cancelled_Amount > 0
GROUP BY Borrower, Project_Name, Project_ID, Cancelled_Amount, Service_Charge_Rate
ORDER BY Cancelled_Amount DESC;

----------------To find The Average Interest Offered by the Kenyan Government -----
SELECT sum(Interest_Rate) AS "Interest_Sum",
    round(avg(Interest_Rate), 0) AS "Interest_Average"  
FROM [dbo].[IBRD_Loans_to_Kenya]
WHERE Guarantor = 'Kenya'

--------To find the Average amount of money loaned to Kenyan Projects from the United Kingdom-------
SELECT sum(Disbursed_Amount) AS "Given_Sum",
    round(avg(Disbursed_Amount), 0) AS "Disbursed_Average"  
FROM [dbo].[IBRD_Loans_to_Kenya]
WHERE Guarantor = 'United Kingdom'

--------The Amount of Money Approved by Board but have Pending Projects ---------
SELECT sum(Total_IFC_investment_as_approved_by_Board_Million_USD) AS "Given_Sum_In_Millions"
FROM [dbo].[IFC_Investment_Projects_in_Kenya]
WHERE Status = 'Pending'

--------------Joining The Queries to find the sum of the Total Loans and Credits Repaid ---------
SELECT SUM(Repaid_to_IBRD) AS Total_Loan_Paid
FROM [dbo].[IBRD_Loans_to_Kenya] 
JOIN [dbo].[IDA_Credits___Grants_to_Kenya] 
ON [dbo].[IDA_Credits___Grants_to_Kenya].SUM[Repaid_to_IDA] = [dbo].[IBRD_Loans_to_Kenya].SUM[Repaid_to_IBRD]


