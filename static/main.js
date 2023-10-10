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
      image_url: imageUrl
    }
  );

  const $cupcake = makeCupcakeElement(newCupcake);

  $cupcake.prependTo($cupcakes);

}

/**
 * Takes a cupcake instance and
 * returns a JQuery object for the cupcake.
 */

function makeCupcakeElement(cupcake){
  const html = `
    <li id="${cupcake.id}">
      <h2>${cupcake.flavor}</h2>
      <img src="${cupcake.imageUrl}">
      <ul>
        <li>Size: ${cupcake.size}</li>
        <li>Rating: ${cupcake.rating}</li>
      </ul>
      <button class="delete" data-cupcake-id="${cupcake.id}">Delete</button>
    </li>
  `

  return $(html)
}

/**
 * Gets and displays all cupcakes.
 */

async function getAndDisplayCupcakes(){
  cupcakesList = await CupcakeList.getCupcakes();

  for (const cupcake of cupcakesList.cupcakes) {
    const $cupcake = makeCupcakeElement(cupcake);
    $cupcake.appendTo($cupcakes);
  }
}

/**
 * Handles deleting cupcake
 */

async function handleDeleteCupcake(evt) {
  const $button = $(evt.target);
  const cupcakeId = $button.data("cupcake-id");

  const deletedCupcakeId = await cupcakesList.deleteCupcake(cupcakeId);

  $button.closest(`li`).remove();
}

$newCupcakeForm.on("submit", handleSubmitForm);
$cupcakes.on("click", ".delete", handleDeleteCupcake)

getAndDisplayCupcakes();