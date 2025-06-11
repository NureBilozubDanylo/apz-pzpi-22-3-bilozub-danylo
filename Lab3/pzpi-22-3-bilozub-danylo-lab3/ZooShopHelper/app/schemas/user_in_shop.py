from pydantic import BaseModel

class UserInShopBase(BaseModel):
    user_id: int
    shop_id: int
    model_config = {
        "from_attributes": True
    }

class UserInShopCreate(UserInShopBase):
    pass

class UserInShopUpdate(UserInShopBase):
    pass

class UserInShop(UserInShopBase):
    user_in_shop_id: int

    model_config = {
        "from_attributes": True
    }
