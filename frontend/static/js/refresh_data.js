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
							var figure = document.createElement("figure");

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