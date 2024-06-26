$(document).ready(function () {
    $("#reviewform").submit(function (e) {
        e.preventDefault();

        $.ajax({
            data: $(this).serialize(),
            method: $(this).attr("method"),
            url: $(this).attr("action"),
            dataType: "json",
            success: function (response) {
                console.log("comment saved", response);

                if (response.bool === true) {
                    $("#review-comment").html("<h2>Review Added successfully</h2>");
                    $(".hide-comment-form").hide();

                    let context = response.context;
                    let created_at = new Date().toLocaleDateString('en-GB', {
                        day: '2-digit',
                        month: 'short',
                        year: 'numeric'
                    });

                    // Construct a unique ID for the new comment
                    let commentId = `comments-${context.id}`;

                    // Check if the comment already exists
                    if ($(`#${commentId}`).length === 0) {
                        let _html = `
                          <li class="comment-list" id="${commentId}">
                            <div class="comment-avatar text-center">
                              <img src="${staticUrl}" alt="" />
                              <div class="product-rating mt-10">
                                ${generateStarRating(context.rating)}
                              </div>
                            </div>
                            <div class="comment-desc">
                              <span>${created_at}</span>
                              <h4>${context.user.name}</h4>
                              <p>${context.review}</p>
                            </div>
                          </li>`;

                        // Prepend to the correct parent element containing the list of comments
                        $(".comments-container").prepend(_html);
                    } else {
                        console.log("Comment already exists.");
                    }
                } else {
                    console.error("Failed to save comment:", response.errors);
                }
            },
            error: function (xhr, status, error) {
                console.error("AJAX error:", status, error);
            }
        });
    });

    function generateStarRating(rating) {
        let fullStars = Math.floor(rating);
        let emptyStars = 5 - fullStars;

        let starHtml = '';

        for (let i = 0; i < fullStars; i++) {
            starHtml += '<i class="fa fa-star"></i>'; // Full star
        }

        for (let i = 0; i < emptyStars; i++) {
            starHtml += '<i class="fa fa-star-o"></i>'; // Empty star
        }

        return starHtml;
    }
});



// --------------------------------------fiilter product
$(document).ready(function () {
    // Event handler for clicking on filter checkboxes or the price filter button
    $(".filter-checkbox, #price-filter-btn").on("click", function () {
        console.log("Checkbox or button clicked");

        // Initialize an empty object to hold the filter criteria
        let filter_object = {};

        // Get the minimum price from the min attribute of the price input element
        let min_price = $("#max_price").attr("min");
        // Get the current value of the price input element
        let max_price = $("#max_price").val();

        // Add price filters to the filter object only if they are set
        if (min_price) {
            filter_object.min_price = min_price;
        }
        if (max_price) {
            filter_object.max_price = max_price;
        }

        // Iterate over each filter checkbox
        $(".filter-checkbox").each(function () {
            // Get the filter key from the data-filter attribute
            let filter_key = $(this).data("filter");
            // Create an array of checked values for the current filter key
            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter="' + filter_key + '"]:checked')).map(function (element) {
                return element.value;
            });
        });

        console.log("Filter object is ", filter_object);

        // Send an AJAX request to the server with the filter criteria
        $.ajax({
            url: "/filter-product", // URL to send the request to
            data: filter_object, // Data to be sent to the server
            dataType: "json", // Expect a JSON response from the server
            beforeSend: function () {
                console.log("Before send");
            },
            // Function to handle a successful response
            success: function (response) {
                console.log("Success");
                console.log(response);
                // Update the HTML content of the element with id 'filtered-product' with the response data
                $("#filtered-product").html(response.data);
            },
            // Function to handle errors
            error: function (xhr, status, error) {
                console.log("Error: ", error);
            }
        });
    });

    // Event handler for when the price input loses focus
    $("#max_price").on("blur", function () {
        let min_price = $(this).attr("min"); // Get the minimum price value
        let max_price = $(this).attr("max"); // Get the maximum price value
        let current_price = $(this).val(); // Get the current price value

        console.log(min_price, max_price, current_price);
        // Check if the current price is outside the allowed range
        if (current_price < parseInt(min_price) || current_price > parseInt(max_price)) {
            console.log("Error occurred");

            // Round the minimum and maximum prices to two decimal places
            min_price = Math.round(min_price * 100) / 100;
            max_price = Math.round(max_price * 100) / 100;

            // Alert the user about the allowed price range
            alert("Price must be between $" + min_price + " and $" + max_price);
            // Reset the price input value to the minimum price
            $(this).val(min_price);
            // Reset the range input value to the minimum price
            $("#range").val(min_price);
            // Refocus the price input
            $(this).focus();

            return false; // Prevent further execution
        }
    });



    // ----------------------------- Add to cart

    $(".add-to-cart-btn").on("click", function () {
        let this_val = $(this)
        let index = this_val.attr("data-index")

        let quantity = $(".product-quantity-" + index).val()
        let product_title = $(".product-title-" + index).val()

        let product_id = $(".product-pid-" + index).val()
        let product_price = $("#product-price-" + index).text()

        let product_image = $(".product-image-" + index).val()


        console.log("Quantity", quantity)
        console.log("Product id", product_id)
        console.log("product price", product_price)
        console.log("product titile", product_title)
        console.log("current element", this_val)
        console.log("current index", index)
        console.log("product image", product_image)

        $.ajax({
            url: "/ecommerce/add-to-cart",
            data: {
                "id": product_id,
                "qty": quantity,
                "image": product_image,
                "title": product_title,
                "price": product_price
            },
            dataType: "json",
            beforeSend: function () {
                this_val.html("Adding...")
                console.log("Adding product to cart")
            },
            success: function (response) {
                console.log("Success")
                console.log(response)
                this_val.html("Added 👍")
                console.log("Added product to cart")
                $(".cart-item-count").text(response.totalcartitems)
                console.log("Updated cart item count:", response.totalcartitems)
            }




        })
    });



    // ----------------------------- delete product from cart list

    $(document).ready(function () {
        function attachHandlers() {
            // Attach delete handlers
            $(".delete-product").off("click").on("click", function (e) {
                e.preventDefault(); // Prevent the default action
                let product_id = $(this).data("product");
                let this_value = $(this);

                console.log("product id ", product_id);

                $.ajax({
                    url: "/ecommerce/delete-from-cart", // Ensure this URL matches your Django URL pattern
                    data: {
                        "id": product_id
                    },
                    dataType: "json",
                    beforeSend: function () {
                        this_value.hide(); // Hide the delete button before sending the request
                    },
                    success: function (response) {
                        $(".cart-item-count").text(response.totalcartitems); // Update the cart item count
                        $("#cart-list").html(response.data); // Update the cart list with new data
                        attachHandlers(); // Re-attach handlers to the new elements
                    },
                    error: function (xhr, status, error) {
                        console.error('Error deleting item from cart:', error);
                        this_value.show(); // Show the delete button again in case of an error
                    }
                });
            });

            // Attach update handlers
            $(".update-product").off("click").on("click", function (e) {
                e.preventDefault(); // Prevent the default action
                let product_id = $(this).data("product");
                let new_quantity = $(this).closest("tr").find("input[type='text']").val();
                let this_value = $(this);

                console.log("product id ", product_id);
                console.log("new quantity ", new_quantity);

                $.ajax({
                    url: "/ecommerce/update-to-cart", // Ensure this URL matches your Django URL pattern
                    data: {
                        "id": product_id,
                        "quantity": new_quantity // Include the new quantity in the request
                    },
                    dataType: "json",
                    beforeSend: function () {
                        this_value.hide(); // Hide the update button before sending the request
                    },
                    success: function (response) {
                        $(".cart-item-count").text(response.totalcartitems); // Update the cart item count
                        $("#cart-list").html(response.data); // Update the cart list with new data
                        attachHandlers(); // Re-attach handlers to the new elements
                    },
                    error: function (xhr, status, error) {
                        console.error('Error updating item in cart:', error);
                        this_value.show(); // Show the update button again in case of an error
                    }
                });
            });
        }

        // Initial attachment of event handlers
        attachHandlers();
    });


    // Add product to wishlist
    $(".add-to-wishlist").on("click", function () {
        let this_val = $(this)
        let product_id = $(this).attr("data-product-item")


        console.log("product id ", product_id);
        console.log("this val ", this_val);

        $.ajax({
            url: "/ecommerce/add-to-wishlist",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function () {
                this_val.html("❤️")
                console.log("Adding product to wishlist");
            },
            success: function (response) {
               if(response.bool === true){
                console.log("Success")
                console.log(response)

                this_val.html("❤️")
                console.log("Added product to wishlist")
                $(".wishlist-item-count").text(response.totalwishlistitems)

               }
            }
        })




    })

});



document.addEventListener("DOMContentLoaded", function() {
    var countdownElements = document.querySelectorAll("[data-countdown-end]");

    countdownElements.forEach(function(element) {
        var endTime = new Date(element.getAttribute("data-countdown-end")).getTime();
        countdownTimer(endTime, element);
    });
});

function countdownTimer(endTime, element) {
    var x = setInterval(function() {
        var now = new Date().getTime();
        var distance = endTime - now;

        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        element.innerHTML = days + "d " + hours + "h " + minutes + "m " + seconds + "s ";

        if (distance < 0) {
            clearInterval(x);
            element.innerHTML = "EXPIRED";
        }
    }, 1000);
}
