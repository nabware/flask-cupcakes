"use strict";

const $newCupcakeForm = $('#new-cupcake-form');
const $cupcakes = $('#cupcakes');
let cupcakesList;

/**
 * Handles new cupcake form submit
 */

async function handleSubmitForm(evt) {
  evt.preventDefault();

  const flavor = $("#flavor-input").val();
  const size = $("#size-input").val();
  const rating = $("#rating-input").val();
  const imageUrl = $("#image-url-input").val();

  const newCupcake = await cupcakesList.addCupcake(
    {
      flavor,
      size,
      rating,
      imageUrl
    }
  );

  $("<li>").text(newCupcake.flavor).prependTo($cupcakes);
}

/**
 * Gets and displays all cupcakes.
 */

async function getAndDisplayCupcakes(){
  cupcakesList = await CupcakeList.getCupcakes();

  for (const cupcake of cupcakesList.cupcakes) {
    $("<li>").text(cupcake.flavor).appendTo($cupcakes);
  }
}

$newCupcakeForm.on("submit", handleSubmitForm);

getAndDisplayCupcakes();