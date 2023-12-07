document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').onsubmit = send;
  

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
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

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  get_emails(mailbox);
}

function send() {
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  console.log(recipients)
  console.log(subject)
  console.log(body)
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent');
  });
  return false;
}

function get_emails(mailbox) {
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      for (let i = 0; i < emails.length; i++) {
        let mail = emails[i]
        const element = document.createElement('div');
        element.className = 'mailDiv';
        if (mailbox === 'sent') {
          element.innerHTML = `To: ${mail.recipients} <br> Subject: ${mail.subject} <br> ${mail.timestamp}`;
        }
        else {
          element.innerHTML = `From: ${mail.sender} <br> Subject: ${mail.subject} <br> ${mail.timestamp}`;
        }
        if (mail.read === true) {
          element.style.background = 'gray';
          element.style.color = 'white';
        }
        else if (mail.read === false) {
          element.style.background = 'white';
        }
        element.addEventListener('click', function() {
          fetch(`/emails/${mail.id}`)
          .then(response => response.json())
          .then(email => {
              // Print email
              console.log(email);
          
              const elements = document.querySelectorAll('.mailDiv');
              const title = document.querySelector('h3');
              title.remove();
              elements.forEach(element => {
                element.remove();
              });

              const mailView = document.createElement('div');
              mailView.className = 'mailDiv';
              mailView.innerHTML = `From: ${mail.sender} <br> To: ${mail.recipients} <br> Subject: ${mail.subject} <br> ${mail.timestamp} <hr> ${mail.body}`;
              document.querySelector('#emails-view').append(mailView);
              fetch(`/emails/${mail.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    read: true
                })
              })
              

              if (mailbox === 'inbox') {
                const archiveBtn = document.createElement('button');
                archiveBtn.innerHTML = 'Archive';
                archiveBtn.classList.add('btn', 'btn-primary', 'mr-2')
                document.querySelector('#emails-view').append(archiveBtn);
                archiveBtn.addEventListener('click', function() {
                  fetch(`/emails/${mail.id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        archived: true
                    })
                  })
                  load_mailbox('inbox');
                })
                const replyBtn = document.createElement('button');
                replyBtn.innerHTML = 'Reply';
                replyBtn.classList.add('btn', 'btn-primary');
                document.querySelector('#emails-view').append(replyBtn);
                replyBtn.addEventListener('click', function() {
                  // take me to the composition form with the recipient field prefilled
                  compose_email()
                  document.querySelector('#compose-recipients').value = mail.sender;
                  document.querySelector('#compose-subject').value = mail.subject.slice(0,4)==="Re: " ? mail.subject : "Re: " + mail.subject;
                  document.querySelector('#compose-body').value = `"On ${mail.timestamp} ${mail.sender} wrote: ${mail.body}"`;
                })
              }


              else if (mailbox === 'archive') {
                const unArchiveBtn = document.createElement('button');
                unArchiveBtn.innerHTML = 'Unarchive';
                unArchiveBtn.classList.add('btn', 'btn-primary')
                document.querySelector('#emails-view').append(unArchiveBtn);
                unArchiveBtn.addEventListener('click', function() {
                  fetch(`/emails/${mail.id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        archived: false
                    })
                  })
                  load_mailbox('inbox');
                })
              }
              
          });
        });
        document.querySelector('#emails-view').append(element);
      }
  });
}