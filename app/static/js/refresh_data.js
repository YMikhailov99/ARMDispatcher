function show()
		{
			$.ajax({
				url: "/incoming_calls",
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
							vp.textContent ="ВП: " + data[i].description;
							div.appendChild(vp);

							var address = document.createElement("p");
							address.textContent ="Адрес: " + data[i].name_and_address;
							div.appendChild(address);

							var reglament = document.createElement("p");
							reglament.textContent ="Регламент: " + data[i].description_1;
							div.appendChild(reglament);

							var RemoveCard_button = document.createElement("button");
							RemoveCard_button.textContent = "Убрать карточку";
							RemoveCard_button.className = "emergency";
							div.appendChild(RemoveCard_button);
							RemoveCard_button.value = ["Убрать", data[i].gsm_number_vp || data[i].sip_number_vp, data[i].id];
							RemoveCard_button.onclick = asyncSendCloseRequestManually;

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
							var divim1 = document.createElement("div");
							img1.src ="video_feed?src="+ encodeURIComponent(data[i].camera_url);
							img1.loading = "lazy"
							img1.className = "mh-100";
							var img2 = document.createElement("img");
							img2.src =data[i].camdirect_url;
							img2.src ="video_feed?src="+ encodeURIComponent(data[i].camdirect_url);
							img1.loading = "lazy"
							div.appendChild(document.createElement("br"))
							div.appendChild(img1)
							div.appendChild(img2)

							var buttons = div.querySelectorAll(".team-row button");
								for (let j =1; j<buttons.length; j++)
								{
									buttons[j].value = [buttons[j].textContent, data[i].gsm_number_vp || data[i].sip_number_vp, data[i].id];
									buttons[j].onclick = sendOpenRequestToCore;
								}
							li.appendChild(div);
							li.setAttribute("id", id);
							li.className="col-12 col-sm-12 col-md-6 col-lg-6 col-xl-6"

							/*var OpBtn = document.createElement("button");
							OpBtn.textContent = "Подтвердить открытие";
							OpBtn.className = "BottomBtn";
							li.appendChild(OpBtn);

							var HttpBtn = document.createElement("button");
							HttpBtn.textContent = "HTTP";
							HttpBtn.className = "BottomBtn";
							li.appendChild(HttpBtn);*/

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
				url: '/open_barrier_by_core',
				method: 'get',
				dataType: 'html',
				data: {button_name: parameters[0], barrier_number: parameters[1]},
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
							if(parameters[2] == ul_child_id){
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
async function asyncSendCloseRequestManually(){
	var parameters = event.srcElement.value.replace('[', '').replace(']', '').split(',');
	var Open_button = event.srcElement;
	await sendCloseRequestManually(parameters, Open_button)
}
function sendOpenRequestManually() {
	var parameters = event.srcElement.value.replace('[', '').replace(']', '').split(',');
	var Open_button = event.srcElement;
			$.ajax({
				url: '/open_manually',
				method: 'get',
				dataType: 'html',
				data: {button_name: parameters[0], barrier_number: parameters[1]},
				success: function(response){
					response = JSON.parse(response)
					if(response){
						var ul = document.getElementById("list");
						var ul_children = ul.children;
						for(var i = 0; i<ul_children.length; i++) {
							var ul_child_id = ul_children[i].getAttribute('id').slice(7);
							if(parameters[2] == ul_child_id){
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

async function sendCloseRequestManually(parameters, Close_button) {
			await $.ajax({
				url: '/close_manually',
				method: 'get',
				async: true,
				dataType: 'html',
				data: {button_name: parameters[0], barrier_number: parameters[1]},
				success: function(response){
					response = JSON.parse(response)
					if(response){
						var ul = document.getElementById("list");
						var ul_children = ul.children;
						for(var i = 0; i<ul_children.length; i++) {
							var ul_child_id = ul_children[i].getAttribute('id').slice(7);
							if(parameters[2] == ul_child_id){
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