```mermaid
classDiagram
class PresentationLayer {
    <<Interface>>
    +ServiceAPI
}
class BusinessLogicLayer {
    +UserEntity
    +PlaceEntity
    +ReviewEntity
    +AmentityEntity
}
class PersistenceLayer {
    +DatabaseAccess

}
PresentationLayer --> BusinessLogicLayer : Facade Pattern
BusinessLogicLayer --> PersistenceLayer : Database Operations
```


Presentation Layer: 
- top layer, contains the API
- only interaction the user has is through this
- sends request to BL and returns failure or success e.g. user clicks edit property, sends request to BL and gets returned sucess or failure
- only talks to the BL, doesnt know of persistence layers existence 

Business Logic Layer: 
- Holds main Entities
- Holds all the logic and connections between each entity. e.g. only X user edit thise property
- talks to both layers, though only sends requests to persistence if passes logic

Persistence Layer: 
- handles the connection to database
- deals with all the read and write for the database e.g. changing the values of said property owner wants
- doesnt know of any logic above only does the task given

Facade Pattern:
- Alot of small highly focused code (def for each single task) vs one class doing everything
  
```mermaid
classDiagram

class User {
    +UUID id
    +String first_name
    +String last_name
    +String email
    +String password
    +Boolean is_admin
    +DateTime created_at
    +DateTime updated_at
    +register()
    +update_profile()
    +delete()
}

class Place {
    +UUID id
    +String title
    +String description
    +Float price
    +Float latitude
    +Float longitude
    +DateTime created_at
    +DateTime updated_at
    +create()
    +update()
    +delete()
    +list()
    +add_amenity()
    +remove_amenity()
}

class Review {
    +UUID id
    +Integer rating
    +String comment
    +DateTime created_at
    +DateTime updated_at
    +create()
    +update()
    +delete()
    +list_by_place()
}

class Amenity {
    +UUID id
    +String name
    +String description
    +DateTime created_at
    +DateTime updated_at
    +create()
    +update()
    +delete()
    +list()
}

User "1" --> "0..*" Place : owns
User "1" --> "0..*" Review : writes
Place "1" --> "0..*" Review : receives
Place "0..*" --> "0..*" Amenity : has
Review "1" --> "1" User : author
Review "1" --> "1" Place : for
```