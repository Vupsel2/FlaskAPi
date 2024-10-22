# Cake Catalog API Application

As a bonus, an endpoint has been added to assign cakes to bakeries.

## List of Endpoints

### Cakes

- **Get all cakes**  
  `GET /api/v1/cakes`
  - Optional query parameters: `flavor`, `max_price`, `page`, `limit`

- **Get a specific cake by ID**  
  `GET /api/v1/cakes/{id}`

- **Create a new cake**  
  `POST /api/v1/cakes`
  - Request body:
    ```json
    {
      "name": "Chocolate Cake",
      "flavor": "Chocolate",
      "price": 15.99,
      "available": true
    }
    ```

- **Update a cake**  
  `PUT /api/v1/cakes/{id}`
  - Request body:
    ```json
    {
      "name": "Vanilla Cake",
      "flavor": "Vanilla",
      "price": 12.99,
      "available": true
    }
    ```

- **Delete a cake**  
  `DELETE /api/v1/cakes/{id}`

### Bakeries

- **Get all bakeries**  
  `GET /api/v1/bakeries`

- **Get a specific bakery by ID**  
  `GET /api/v1/bakeries/{id}`

- **Create a new bakery**  
  `POST /api/v1/bakeries`
  - Request body:
    ```json
    {
      "name": "Sweet Delights",
      "location": "123 Bakery Street",
      "rating": 5
    }
    ```

- **Update a bakery**  
  `PUT /api/v1/bakeries/{id}`
  - Request body:
    ```json
    {
      "name": "Sweet Delights Bakery",
      "location": "456 New Street",
      "rating": 4
    }
    ```

- **Delete a bakery**  
  `DELETE /api/v1/bakeries/{id}`

### Bakery and Cakes Association

- **Get all cakes for a specific bakery**  
  `GET /api/v1/bakeries/{id}/cakes`

- **Assign a cake to a bakery(Bonus)**  
  `POST /api/v1/bakeries/{bakery_id}/cakes/{cake_id}`
