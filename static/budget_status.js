Javascript 

// budget status function

// for budget in budgets
// if budget end_date is > datetime.now()
//            for transaction in transactions
//                  if transaction.merchant_name === budget.merchant_name and transaction.date > budget.start_date and transaction.date < budget.end_date
//                      if sum (transaction.amout) > budget.amount
//                          return  you went over budget for {budget.merchant_name} and tree died image. 
//                      else if sum (transaction.amout) < budget.amount or sum (transaction.amout) === budget.amount 
//                          return Good job! you are in budget for {budget.merchant_name} and livingtree image.
//          
