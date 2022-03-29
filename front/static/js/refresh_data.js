function show()
		{
			$.ajax({
				url: "http://127.0.0.1:8000/incoming_calls",
				cache: false,
				success: function(json){
					let data = JSON.parse(json);
					var ul = document.getElementById("list");
					var ul_children = ul.children;
					for(var i = 0; i<ul_children.length; i++) {
						var a = ul_children[i].getAttribute('id').slice(7);
						if(!data.find(d=>d.id == a)){
							ul.removeChild(ul_children[i])
							i--;
						}
					}
					for(var i = 0; i<data.length; i++){
						var id = "element"+data[i].id;
						if(document.getElementById(id) == null)
						{
							var li = document.createElement("li");
							var div = document.createElement("div");
							div.className = "team-row";
							var vp = document.createElement("p");
							vp.textContent ="ВП: " + data[i].number;
							div.appendChild(vp);

							var address = document.createElement("p");
							address.textContent ="Адрес: " + data[i].object_name_and_address;
							div.appendChild(address);

							var reglament = document.createElement("p");
							reglament.textContent ="Регламент: " + data[i].description;
							div.appendChild(reglament);


							var Departure_button = document.createElement("button");
							Departure_button.textContent = "Выезд";
							var JKH_button = document.createElement("button");
							JKH_button.textContent = "ЖКХ";
							var Delivery_button = document.createElement("button");
							Delivery_button.textContent = "Доставка";
							var Collection_button = document.createElement("button");
							Collection_button.textContent = "Инкассация";
							var Garbage_truck_button = document.createElement("button");
							Garbage_truck_button.textContent = "Мусоровоз";
							var Post_button = document.createElement("button");
							Post_button.textContent = "Почта";
							var Taxi_button = document.createElement("button");
							Taxi_button.textContent = "Такси";

							if(!data[i].is_free_departure_prohibited){
								div.appendChild(Departure_button)
							}
							if(!data[i].is_free_jkh_passage_prohibited){
								div.appendChild(JKH_button)
							}
							if(!data[i].is_free_delivery_passage_prohibited){
								div.appendChild(Delivery_button)
							}
							if(!data[i].is_free_collection_passage_prohibited){
								div.appendChild(Collection_button)
							}
							if(!data[i].is_free_garbtrucks_passage_prohibited){
								div.appendChild(Garbage_truck_button)
							}
							if(!data[i].is_free_post_passage_prohibited){
								div.appendChild(Post_button)
							}
							if(!data[i].is_free_taxi_passage_prohibited){
								div.appendChild(Taxi_button)
							}
							var img1 = document.createElement("img");
							img1.src =data[i].camera_url;
							var img2 = document.createElement("img");
							img2.src =data[i].camdirect_url;
							div.appendChild(document.createElement("br"))
							div.appendChild(img1)
							div.appendChild(img2)

							var buttons = div.querySelectorAll(".team-row button");
								for (let j =0; j<buttons.length; j++)
								{
									buttons[j].value = [buttons[j].textContent, data[i].id];
									buttons[j].onclick = sendOpenRequestToCore;
								}
							li.appendChild(div);
							li.setAttribute("id", id);
							ul.appendChild(li);
						}
					}
				}
			});
		}

		$(document).ready(function(){
			show();
			setInterval('show()',1000);
		});

function sendOpenRequestToCore() {
	var parameters = event.srcElement.value.replace('[', '').replace(']', '').split(',');

			$.ajax({
				url: 'http://127.0.0.1:8000/open_barrier_by_core',
				method: 'get',
				dataType: 'html',
				data: {button_name: parameters[0], barrier_id: parameters[1]},
				success: function(response){
					response = JSON.parse(response)
					if(response){
						window.alert("Шлагбаум с id = " + parameters[1] + " открыт");
					}
					else {
						window.alert("Шлагбаум с id = " + parameters[1] + " открыть не удалось");
						var ul = document.getElementById("list");
						var ul_children = ul.children;
						for(var i = 0; i<ul_children.length; i++) {
							var ul_child_id = ul_children[i].getAttribute('id').slice(7);
							if(parameters[1] == ul_child_id){
								var Open_mannually_button = document.createElement("button");
								Open_mannually_button.textContent = "Открыть напрямую";
								Open_mannually_button.value = parameters;
								Open_mannually_button.style["background-color"] = "#f00";
								Open_mannually_button.onclick = sendOpenRequestManually;
								ul_children[i].appendChild(Open_mannually_button);
							}
						}
					}
					}
			});
        }

function sendOpenRequestManually() {
	var parameters = event.srcElement.value.replace('[', '').replace(']', '').split(',');
	var Open_button = event.srcElement;
			$.ajax({
				url: 'http://127.0.0.1:8000/open_manually',
				method: 'get',
				dataType: 'html',
				data: {button_name: parameters[0], barrier_id: parameters[1]},
				success: function(response){
					response = JSON.parse(response)
					if(response){
						var ul = document.getElementById("list");
						var ul_children = ul.children;
						for(var i = 0; i<ul_children.length; i++) {
							var ul_child_id = ul_children[i].getAttribute('id').slice(7);
							if(parameters[1] == ul_child_id){
								var Close_mannually_button = document.createElement("button");
								Close_mannually_button.textContent = "Закрыть";
								Close_mannually_button.style["background-color"] = "#f00";
								Close_mannually_button.onclick = sendCloseRequestManually;
								Close_mannually_button.value = parameters;
								ul_children[i].appendChild(Close_mannually_button);
								ul_children[i].removeChild(Open_button);
							}
						}
					}
					else {
						window.alert("Шлагбаум с id = " + parameters[1] + " открыть не удалось");

					}
					}
			});
        }

function sendCloseRequestManually() {
	var parameters = event.srcElement.value.replace('[', '').replace(']', '').split(',');
	var Close_button = event.srcElement;
			$.ajax({
				url: 'http://127.0.0.1:8000/close_manually',
				method: 'get',
				dataType: 'html',
				data: {button_name: parameters[0], barrier_id: parameters[1]},
				success: function(response){
					response = JSON.parse(response)
					if(response){
						var ul = document.getElementById("list");
						var ul_children = ul.children;
						for(var i = 0; i<ul_children.length; i++) {
							var ul_child_id = ul_children[i].getAttribute('id').slice(7);
							if(parameters[1] == ul_child_id){
								ul_children[i].removeChild(Close_button);
							}
						}
					}
					else {
						window.alert("Шлагбаум с id = " + parameters[1] + " закрыть не удалось");
					}
					}
			});
        } 