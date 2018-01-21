pragma solidity ^0.4.18;

contract database{
    event registered(address);
  struct User{
  	string name;
  	bytes aadhar_number;
  	bytes password;
  	bytes username;
  	bytes portfolio;
  	bytes publickey;
  	bytes privatekey;
  }
 struct GovApplication{
        bytes documentHash;
        string name;
        bytes encryptedHash;
        string portfolio;
    }

  mapping(address=>User) public users;
  mapping(address=>GovApplication[]) public orders;
  address[] users_addr;
  function compareBytes(bytes a,bytes b) public constant returns (bool){
      if (a.length != b.length)
			return false;
		// @todo unroll this loop
		for (uint i = 0; i < a.length; i ++)
			if (a[i] != b[i])
				return false;
		return true;
  }

  function login(bytes username,bytes password) public returns (address){
    for(uint i=0;i<users_addr.length;i++){
        if(compareBytes(users[users_addr[i]].username,username)){
            if(compareBytes(users[users_addr[i]].password,password)){
  			return users_addr[i];
  			}
  	}
    }
  	return 0;
  }

  function register(bytes _username,bytes _password,bytes _aadhar_number,string _name,bytes _portfolio,bytes publik ,bytes privatek,address user_addr) public returns (string){
  	users[user_addr] = User({
  		name:_name,
  		username:_username,
  		password:_password,
  		aadhar_number:_aadhar_number,
  		portfolio:_portfolio,
  		publickey:publik,
  		privatekey:privatek
  		});
  	users_addr.push(user_addr);
  	return "User Successfully Created";
  }

  function getPublicKey(address userd) public constant returns (bytes){
      return users[userd].publickey;
  }

  function getPrivateKey() public constant returns(bytes){
      return users[msg.sender].privatekey;
  }

  function getGovApplication(address useraddr, uint cursor) constant public returns (string,string){
      GovApplication memory application  = orders[useraddr][cursor];
      return (application.name,application.portfolio);
  }

  function getCurrentUser(address useraddr) public constant returns (string,bytes,bytes,bytes,bytes){
  	User memory user = users[useraddr];
  	return (user.name,user.aadhar_number,user.password,user.username,user.portfolio);
  }

  function uploadHash(bytes hash,string _name,bytes enchash) public {
      orders[msg.sender].push(GovApplication({
          documentHash:hash,
          name:_name,
          encryptedHash:enchash,
          portfolio:""
      }));
  }
  function updateHash(bytes hash,bytes enchash,string portfolio_,address user_addr_) public returns (string){
      GovApplication[] memory applications = orders[user_addr_];
      for(uint i=0;i<applications.length;i++){
          if(compareBytes(applications[i].documentHash,hash)){
              applications[i].encryptedHash = enchash;
              applications[i].portfolio = portfolio_;
              return 'Stored';
          }
      }
  }


}
