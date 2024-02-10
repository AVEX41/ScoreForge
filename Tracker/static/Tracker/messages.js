function ShowMessage(type, content) {
   // Create the alert div element
    var alertDiv = document.createElement("div");
    alertDiv.classList.add("alert", "alert-" + type, "alert-dismissible", "fade", "show");
    alertDiv.setAttribute("role", "alert");

    // Add the text node for the message
    var messageText = document.createTextNode(content);
    alertDiv.appendChild(messageText);

    // Create the close button
    var closeButton = document.createElement("button");
    closeButton.setAttribute("type", "button");
    closeButton.classList.add("close");
    closeButton.setAttribute("data-dismiss", "alert");
    closeButton.setAttribute("aria-label", "Close");

    // Add the close symbol to the button
    var closeSymbol = document.createElement("span");
    closeSymbol.setAttribute("aria-hidden", "true");
    closeSymbol.innerHTML = "&times;";
    closeButton.appendChild(closeSymbol);

    // Append the close button to the alert div
    alertDiv.appendChild(closeButton);

    // Get the element with the id "messages"
    var messagesElement = document.getElementById("messages");

    // Append the alert div to the messages element
    messagesElement.appendChild(alertDiv);
}