function viewController(){
	//Göra om welcomeview till exikverbar code
	
	if(localStorage.token == null){
		document.getElementById("view").innerHTML=document.getElementById("welcomeview").innerHTML;
	}else{
		document.getElementById("view").innerHTML=document.getElementById("profileview").innerHTML;
		reload();
	}

}
function reload(){
	//uppdates personal information
	document.getElementById("pemail").innerHTML = localStorage.email;
	document.getElementById("pfirstname").innerHTML = localStorage.firstname;
	document.getElementById("pfamilyname").innerHTML = localStorage.familyname;
	document.getElementById("pgender").innerHTML = localStorage.gender;
	document.getElementById("pcity").innerHTML = localStorage.city;
	document.getElementById("pcountry").innerHTML = localStorage.country;
	//uppdates personal information in broweser tab
	document.getElementById("bemail").innerHTML = localStorage.bemail;
	document.getElementById("bfirstname").innerHTML = localStorage.bfirstname;
	document.getElementById("bfamilyname").innerHTML = localStorage.bfamilyname;
	document.getElementById("bgender").innerHTML = localStorage.bgender;
	document.getElementById("bcity").innerHTML = localStorage.bcity;
	document.getElementById("bcountry").innerHTML = localStorage.bcountry;

	//uppdates your wall on profilepage
	var res;
	res = serverstub.getUserMessagesByEmail(localStorage.token, localStorage.email);
	document.getElementById("messages").innerHTML = res.data.length > 0 ? "" : "<label>No messeges</label>";
	for(i = 0 ; i < res.data.length; i++){
		document.getElementById("messages").innerHTML += "<label><b>" + res.data[i].writer + "</b>: " + res.data[i].content + "</label><br/>";
	}
	
	//uppdate your browserwall
	if (localStorage.bemail != null){
		res = serverstub.getUserMessagesByEmail(localStorage.token, localStorage.bemail);
		document.getElementById("messagesbrowser").innerHTML = res.data.length > 0 ? "" : "<label>No messeges</label>";
		for(i = 0 ; i < res.data.length; i++){
			document.getElementById("messagesbrowser").innerHTML += "<label><b>" + res.data[i].writer + "</b>: " + res.data[i].content + "</label><br/>";
		}
	}
}
function reloadWall(){
	res = serverstub.getUserMessagesByEmail(localStorage.token, localStorage.email);
	document.getElementById("messages").innerHTML = res.data.length > 0 ? "" : "<label>No messeges</label>";
	for(i = 0 ; i < res.data.length; i++){
		document.getElementById("messages").innerHTML += "<label><b>" + res.data[i].writer + "</b>: " + res.data[i].content + "</label><br/>";
	}
	if(localStorage.bemail != null){
		res = serverstub.getUserMessagesByEmail(localStorage.token, localStorage.bemail);
		document.getElementById("messagesbrowser").innerHTML = res.data.length > 0 ? "" : "<label>No messeges</label>";
		for(i = 0 ; i < res.data.length; i++){
		document.getElementById("messagesbrowser").innerHTML += "<label><b>" + res.data[i].writer + "</b>: " + res.data[i].content + "</label><br/>";
		}
	}else
		var node = document.getElementById('messagesbrowser');
		while (node.hasChildNodes()) {
			node.removeChild(node.firstChild);
		}
		document.getElementById("messagesbrowser").innerHTML = "No currently user";
    }


//used for signinform--------------------------------------------
function loginUser(frm){

	var res = serverstub.signIn(frm.email.value,frm.pass.value);
	alert(res.message);
	if(res.success){
		localStorage.token = res.data;
		//Personal information
		var userInfo = serverstub.getUserDataByToken(localStorage.token);
		localStorage.email = userInfo.data.email;
		localStorage.firstname = userInfo.data.firstname;
		localStorage.familyname = userInfo.data.familyname;
		localStorage.gender = userInfo.data.gender;
		localStorage.city = userInfo.data.city;
		localStorage.country = userInfo.data.country;
		viewController();
	}else{
		alert(res.message);
	}

}


//---------------------------------------------------------------




//used for signupform------------------------------------------

function checkPassword(password1,password2){
	if(password1.value == password2.value){
		return true;
	}else{
		password2.style.borderColor="red";
		return false;
	}
}

function registerUser(frm){
	var password1 = document.getElementById("regpass1");
	var password2 = document.getElementById("regpass2");
		if(checkPassword(password1,password2)){
			var userObject = new Object();
			userObject.email = frm.email.value;
			userObject.password = frm.pass.value;
			userObject.firstname = frm.firstName.value;
			userObject.familyname = frm.familyName.value;
			userObject.gender = frm.gender.value;
			userObject.city = frm.city.value;
			userObject.country = frm.country.value;
			
			//var res = serverstub.signUp(userObject);
            var res = database_helper.addUser(userObject.email, userObject.password, userObject.firstname, userObject.familyname, userObject.gender, userObject.city, userObject.country)
			if(res.success){
				alert('ok');
			}else{
				alert('nej');
				return false;
			}
			return true;
		}else{
			return false;

		}		
}
//-------------------------------------------------------	
function tabSel(index){
	if(index == 0) {
		document.getElementById("home").style.display = "block";
		document.getElementById("browse").style.display = "none";
		document.getElementById("account").style.display = "none";
	}else if(index == 1) {
		document.getElementById("home").style.display = "none";
		document.getElementById("browse").style.display = "block";
		document.getElementById("account").style.display = "none";
	}else if(index == 2) {
		document.getElementById("home").style.display = "none";
		document.getElementById("browse").style.display = "none";
		document.getElementById("account").style.display = "block";
	}
}

//profileview tab account-----------------------------------
function signOut(){
	var res = serverstub.signOut(localStorage.token);
	if(res.success){
		localStorage.removeItem("token");
		localStorage.removeItem("currentUserView");
		location.reload();
		//viewController();
	}else{
		alert(res.message);
		localStorage.removeItem("token");
		localStorage.removeItem("currentUserView");
		location.reload();
		//viewController();
	}
}

function changePass(){
		var oldpass = document.getElementById("oldpass");
		var newpass = document.getElementById("newpass");
		var newrepass = document.getElementById("newrepass");

		if(checkPassword(newpass,newrepass)){
			var res = serverstub.changePassword(localStorage.token,oldpass.value,newpass.value);
				
			if(res.success){
				return true;
			}else{
				alert(res.message);
				oldpass.style.borderColor="red";
				return false;
			}
		
		}else{
			return false;
		}

}
//-------------------------------------------


function postMessage(frm){
		serverstub.postMessage(localStorage.token, frm.message.value, localStorage.email);
		reload();
}

function serachBrowser(frm){
		var userInfo = serverstub.getUserDataByEmail(localStorage.token,frm.browserSearch.value);
		if(userInfo.success){
			localStorage.bemail = userInfo.data.email;
			localStorage.bfirstname = userInfo.data.firstname;
			localStorage.bfamilyname = userInfo.data.familyname;
			localStorage.bgender = userInfo.data.gender;
			localStorage.bcity = userInfo.data.city;
			localStorage.bcountry = userInfo.data.country;
			reload();
			reloadWall();
			return false;
		}else{
			localStorage.removeItem("bemail"); 
			localStorage.removeItem("bfirstname"); 
			localStorage.removeItem("bfamilyname"); 
			localStorage.removeItem("bgender"); 
			localStorage.removeItem("bcity"); 
			localStorage.removeItem("bcountry"); 
			reload();
			reloadWall();
			alert("User doesn't exist");
			return false;
		}
		return false;	
}
function postMessagebrowser(frm){
		if (localStorage.bemail != null){
			serverstub.postMessage(localStorage.token, frm.message.value, localStorage.bemail);
			reloadWall();
		}else{
			alert("you try to post on a wall that has no user");
		}
}
