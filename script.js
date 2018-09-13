var arr = [{{ids}}];
var result = [];

var size = arr.length;
var i = 0;

while (size>i) {
	var friends = API.friends.get({"user_id":arr[i],"count":5000,"fields":"bdate, city, sex"});
	result.push(friends.items);
	i = i + 1;
}

return result;
