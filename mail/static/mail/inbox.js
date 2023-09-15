document.addEventListener('DOMContentLoaded', function() {
  // By default, load the inbox
  load_mailbox('inbox');
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  // Sending emails
  document.querySelector('#compose-form').addEventListener('submit', send_mail);
  // Handle email (view, archive/unarchive, reply)
  document.addEventListener('click', handle_email);

});

// When back arrow is clicked, return to previous page
window.onpopstate = function(event) {
  const section = event.state.section;
  console.log(section);
  if (section === 'load_mailbox') {
    load_mailbox(event.state.mailbox);
  }
  else if (section === 'view_email') {
    view_email(event.state.id, event.state.classList);
  }
  else if (section === 'compose') {
    compose_email();
  }
  else if (section === 'reply_email') {
    reply_email(event.state.id);
  }
}


function compose_email() {

  // Show compose view and hide other views
  history.pushState({section: 'compose'}, "", '/compose');
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('.button_option').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('.button_option').style.display = 'none';

  // Show the mailbox name
  if (mailbox !== 'archive') {
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3> <hr>`;
  }
  else {
    document.querySelector('#emails-view').innerHTML = '<h3>Archived</h3> <hr>';
  }
  // Show all the mails
  history.pushState({section: 'load_mailbox', mailbox: mailbox}, "", mailbox !== 'inbox' ? `/${mailbox}` : "/");
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      if (emails.length === 0) {
        const h3 = document.createElement('h3');
        h3.innerHTML = 'No mails available for now';
        document.querySelector('#emails-view').append(h3);
      }
      else if (mailbox === 'inbox') {
        emails.forEach(email => {processEmail(email, filter='unarchived')});
      }
      else if (mailbox === 'archive') {
        emails.forEach(email => {processEmail(email, filter='archived')});
      }
      // sent case
      else {
        emails.forEach(email => {processEmail(email, filter='sent-case')});
      }})
  .catch(error => {console.log("Error:", error)});
  
}
// Send the email users submit and load the user's sent mailbox;
function send_mail(event) {
    // document.querySelector('#prefill').value = '';
    event.preventDefault();
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value.replace(/^On[\s\S\@]*---\s\n/, ""),
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      // Load the user's sent box
      load_mailbox('sent');  
    })
    .catch(error => {console.log("Error: ", error)});
  
}

// Create email block for each email
function processEmail(email, filter) {
    // Create a div containing 3 div including sender, subject, timestamp
    const block = document.createElement('div');
    const sender = document.createElement('div');
    const subject = document.createElement('div');
    const timestamp = document.createElement('div');
    block.appendChild(sender);
    block.appendChild(subject);
    block.appendChild(timestamp);
    block.classList.add('email');
    block.id = email.id;
    sender.innerHTML = email.sender;
    sender.className = 'email-sender';

    subject.innerHTML = email.subject;
    subject.className = 'email-subject';

    timestamp.innerHTML = email.timestamp;
    timestamp.className = 'email-timestamp';
    // if (email.archived === false) {
    //   block.classList.add("unarchived");
    // }
    // else {
    //   block.classList.add("archived");
    // }
    if (email.read === false) {
      block.classList.add('unread');
    }
    else {
      block.classList.add('read');
    }
    if (filter === 'unarchived' && email.archived  === false) {
      document.querySelector('#emails-view').append(block);
    }
    else if (filter === 'archived' && email.archived === true ) {
      document.querySelector('#emails-view').append(block);
    }
    // sent case
    else if (filter === 'sent-case') {
      block.classList.add('sent-case');
      document.querySelector('#emails-view').append(block);
    }
    
}
// View email

function handle_email(event) {
  const element = event.target;
  // View email
  if (element.classList.contains('email')) {
    view_email(element.id, Array.from(element.classList));
  }
  // Archive email
  else if (element.className === 'archive' || element.className === 'unarchive') {
    archive_email(element);
  }
  // Reply email
  else if (element.className === 'reply') {
    reply_email(element.id);
  }
}

// View email

function view_email(id, classList) {
  history.pushState({section: 'view_email', id: id, classList:  classList}, "", `/view_mail_${id}`);
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true,
    }),
  })
  .catch(error => {console.log('Error: ', error)});
  // Dispay the email-view page, hide other pages
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  if (classList.includes('sent-case')) {
    document.querySelector('.button_option').style.display = 'none';
  }
  else {
    document.querySelector('.button_option').style.display = 'block';
  }
  // Get the email data 
  fetch(`emails/${id}`)
  .then(response => response.json())
  .then(data => {
    const archive = document.querySelector('[data-type="archive"]');
    if (!data.archived) {
      archive.innerHTML = 'Archive Email';
      archive.className = 'archive';
    } else {
      archive.innerHTML = 'Unarchive Email';
      archive.className = 'unarchive';
    }
     // Clear the recipients 
     document.querySelector('#email-recipients').innerHTML = '';
     // Fill the data into email-view page
     document.querySelector('#email-subject').innerHTML = data.subject;
     document.querySelector('#email-sender').innerHTML = data.sender;
     document.querySelector('#email-timestamp').innerHTML = data.timestamp;
     document.querySelector('#email-recipients').innerHTML = data.recipients.join(', ');
     document.querySelector('#email-body').innerHTML = data.body;
    console.log(data.id);
    // data.recipients.forEach(recipient => {
    //   const li = document.createElement('li');
    //   li.innerHTML = recipient; 
    //   document.querySelector('#email-recipients').append(li);
    // });
    document.querySelector('[data-type="archive"]').id = data.id;
    document.querySelector('.reply').id = data.id;

  })
  .catch(error => {console.log("Error: ", error)});    
}

// Archive and unarchive email
function archive_email(button) {
  console.log('Pass');
  fetch(`/emails/${button.id}`)
  .then(response => response.json())
  .then(email => {
    if (email.archived === false) {
      fetch(`/emails/${button.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived : true,
        })
      })
      button.innerHTML = 'Unarchive Email';
      button.className = 'unarchive';
    } else {
      fetch(`/emails/${button.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: false,
        })
      })
      button.innerHTML = 'Archive Email';
      button.className = 'archive';
    }
  });
}

// Reply email
function reply_email(id) {
  compose_email();
  document.querySelector('#compose-id').innerHTML = `<h3>Reply Email</h3>`
  fetch(`emails/${id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#compose-recipients').value = email.sender;
    const subject = document.querySelector('#compose-subject');
    // Email has already been replied
    if (email.subject.startsWith('Re: ')) {
      subject.value = email.subject;
    }
    // No reply yet
    else {
      subject.value = "Re: " + email.subject;
    }
    document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote: \n ${email.body} \n --- `;
  });
  history.pushState({section: 'reply_email', id: id}, "", `/reply_email_${id}`);
}