function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function like(element) {
  let like;
  const csrftoken = getCookie('csrftoken');

  // Check if the user liked the post
  if (element.classList.contains('like')) {
    if (element.classList.contains('has-text-danger')) {
      element.classList.remove('has-text-danger');
      like = -1;
    } else {
      element.classList.add('has-text-danger');
      like = 1;
    }

    const pk = element.lastElementChild.innerHTML;

    fetch(like_url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({
        pk: pk,
      }),
    }).then((response) => {
      if (response.status === 201) {
        // Server parsed code, (un)like went through
        const like_count = element.firstElementChild;
        like_count.innerHTML = parseInt(like_count.innerHTML) + like;
      } else {
        console.log(response.json());
      }
    });
  }
}

function edit(element) {
  // Get post element
  const post = element.parentElement.parentElement;
  const pk = element.parentElement.firstElementChild.lastElementChild.innerHTML; // wtf
  const prevHTML = post.innerHTML;

  // Add textarea for editing, save button and undo button
  post.innerHTML = `
  <header class="card-header">
    <p class="card-header-title">
      Editing Post
    </p>
  </header>
  <div class="card-content">
    <div class="content">
      <div class="field">
        <label class="label">Message</label>
        <div class="control">
        <textarea class="textarea" required id="content-${pk}"></textarea>
      </div>
    </div>
  </div>
  <footer class="card-footer">
    <a class="card-footer-item" id="save-${pk}">Save</a>
    <a class="card-footer-item" id="undo-${pk}">Undo</a>
  </footer>`;

  document.querySelector(`#undo-${pk}`).addEventListener('click', () => {
    post.innerHTML = prevHTML;
  });

  document.querySelector(`#save-${pk}`).addEventListener('click', () => {
    const csrftoken = getCookie('csrftoken');
    const new_content = document.querySelector(`#content-${pk}`).value;

    fetch(edit_url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({
        pk: pk,
        content: new_content,
      }),
    }).then((response) => {
      if (response.status === 200) {
        // Put post back in original state, but with new content
        post.innerHTML = prevHTML;
        document.querySelector(`#content-${pk}`).innerHTML = new_content;
      }
    });
  });
}
