# Bank-API
REST API to get the Bank List and its branch details for a specific branch.


## Assignment

Create a API server :
1. Data can be found in the [repository](https://github.com/Amanskywalker/indian_banks "repository") for the database. 
2. Any Python web framework can be used to create the API service.
Now you can opt to do either of the following
GraphQL
	1.It should support GraphQL calls at ‘/gql’.
	2.It should have a query for querying Bank Branches data with all the sub class data.
Or 
Rest API
1.REST API endpoints to get the Bank List and its branch details for a specific branch.

3. Bonus points for clean code.
4. Bonus points for Test cases.
5. Bonus points for deploying it on services like Heroku.



## API Endpoints


| Endpoints                        | Request Type |    Query parameters    |    Description                            | 
| -------------------------------- | :----------: | :--------------------: | :---------------------------------------: | 
| /api/v1/banks    |     GET      |    	            |         returns list of banks names           |
| /api/v1/branches/:identifier       |     GET      |    identifier   |   returns branch details based on indentifier, the identifier can either be IFSC code or branch name   |

> Added pagination to the response of the list of banks.	

## Database Schema
```
bank=# \d banks
            Table "public.banks"
 Column |         Type          | Modifiers
--------+-----------------------+-----------
 name   | character varying(49) |
 id     | bigint                | not null
Indexes:
    "banks_id_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "branches" CONSTRAINT "branches_banks_fkey" FOREIGN KEY (bank_id) REFERENCES banks(id)

bank=# \d branches
            Table "public.branches"
  Column  |          Type          | Modifiers
----------+------------------------+-----------
 ifsc     | character varying(11)  | not null
 bank_id  | bigint                 |
 branch   | character varying(74)  |
 address  | character varying(195) |
 city     | character varying(50)  |
 district | character varying(50)  |
 state    | character varying(26)  |
Indexes:
    "branches_ifsc_pkey" PRIMARY KEY, btree (ifsc)
Foreign-key constraints:
    "branches_banks_fkey" FOREIGN KEY (bank_id) REFERENCES banks(id)

```

## Models
Created two models one for bank and other for branches.
Created foreign key on bank in branch model to get the reverse relation for bank name.
```
class Banks(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=49)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'banks'


class Branch(models.Model):
    ifsc = models.CharField(max_length=11, primary_key=True, db_index=True)
    bank = models.ForeignKey(Banks, on_delete=models.CASCADE)
    branch = models.CharField(max_length=74, db_index=True)
    address = models.CharField(max_length=195)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=26)

    def __str__(self):
        return self.branch

    class Meta:
        db_table = 'branches'

```
## Views
Added custom pagination to the response of the list of banks .
```
def get(self, request):
        try:
            all_banks = Banks.objects.all()
            serializer = BankSerializer(all_banks, many=True)

            page = int(request.GET.get('page', 1))
            if page <= 0:
                return Response(
                    {"message": "Page number must be greater than zero."},
                    status=status.HTTP_400_BAD_REQUEST)
            
            per_page = 10
            total = all_banks.count()
            last_page = math.ceil(total / per_page)

            if page > last_page:
                return Response(
                    {"message": "No data to show"},
                    status=status.HTTP_200_OK)

            start = (page - 1) * per_page
            end = page * per_page

            return Response({
                "total": total,
                "page": page,
                "lastPage": last_page,
                "data": serializer.data[start:end]
            }, status=status.HTTP_200_OK)
```
Used regex for checking  if the IFSC code is valid or not. 
Also branch details can be searched using branch name.
```
regex = "^[A-Z]{4}0[A-Z0-9]{6}$"
pattern = re.compile(regex)
def get(self, request, identifier):
        try:
            if pattern.match(identifier):
                branches = Branch.objects.filter(ifsc=identifier).first()
                if branches is not None:
                    serializer = BranchSerializer(branches)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({
                    "message": "IFSC code not found"},
                      status=status.HTTP_404_NOT_FOUND)
			 branches = Branch.objects.filter(branch__istartswith=identifier).first()

            if branches is not None:
                serializer = BranchSerializer(branches)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(
                {"message": "Please enter a valid branch name "},
                status=status.HTTP_404_NOT_FOUND)

```

## Demo Link
https://bank-api-655h.onrender.com/api/v1/banks/
