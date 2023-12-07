document.querySelector('#homeBtn').addEventListener('click', () => {
    document.querySelector('#transferDiv').style.display='none';
    document.querySelector('#homeDiv').style.display='block';
    document.querySelector('#contactsDiv').style.display='none';
})


// TRANSFER PAGE

document.querySelector('#transferBtn').addEventListener('click', () => {
    document.querySelector('#transferDiv').style.display='block';
    document.querySelector('#homeDiv').style.display='none';
    document.querySelector('#contactsDiv').style.display='none';

    document.querySelector('#sendMoneyBtn').addEventListener('click', () => {
        const receiver = document.querySelector('#avlbReceiver').value;
        const amount = document.querySelector('#amountSending').value;

        if (amount && amount > 0) {
            fetch('get_balance/')
            .then(response => response.json())
            .then(user => {
                if (user.balance < amount) {
                    alert('Not enough cash for this transaction')
                }
                else {
                    // transfer money and record transaction
                    const request = new Request(
                        '/transfer/',
                        {headers: {'X-CSRFToken': csrftoken}}
                    );
                    fetch(request, {
                        method: 'POST',
                        mode: 'same-origin',
                        body: JSON.stringify({
                            receiver: receiver,
                            amount: amount
                        })
                    }).then(response => response.json())
                    .then(result => {
                        // Print result
                        console.log(result);
                         // if user registered, success
                        if (result.error === 'not enough cash') {
                            alert('Not enough cash for this transaction')
                        }
                        else {
                            document.querySelector('#transferDiv').style.animationPlayState = 'running';
                            document.querySelector('#transferDiv').addEventListener('animationend', () => {
                                window.location.reload();
                            })
                            
                        }
                    });
                }
            })
        }
        else {
            alert('You must provide receiver and amount')
        }
    })
})


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');



// CONTACTS PAGE

document.querySelector('#contactsBtn').addEventListener('click', () => {
    document.querySelector('#transferDiv').style.display='none';
    document.querySelector('#homeDiv').style.display='none';
    document.querySelector('#contactsDiv').style.display='block';

    const elements = document.querySelectorAll('.contact');
    elements.forEach(element => {
        element.remove();
    })
    fetch('get_contacts/')
    .then(response => response.json())
    .then(contacts => {
        for (let i = 0; i < contacts.length; i++) {
            let contact = contacts[i];
            const element = document.createElement('div');
            element.id = `ctc${contact.id}`;
            element.classList = ('contact padding form-control mb-2');
            element.innerHTML = `<strong>${contact.contact}</strong><br>`;

            const delete_btn = document.createElement('button');
            delete_btn.innerHTML = 'Delete';
            delete_btn.classList = ('btn btn-danger m-2')
    
            document.querySelector('#contactsList').append(element);
            document.querySelector(`#ctc${contact.id}`).append(delete_btn);

            // delete contact logic
            delete_btn.addEventListener('click', () => {
                const request = new Request(
                    `/remove_contact/${contact.id}`,
                    {headers: {'X-CSRFToken': csrftoken}}
                );
                fetch(request, {
                    method: 'PUT',
                    mode: 'same-origin',
                    body: JSON.stringify({
                        id: contact.id
                    })
                }).then(() => {
                    window.location.reload();
                    alert('Contact removed')
                })
            })
        }
        
    })


    // Add contact logic
    document.querySelector('#addContactBtn').addEventListener('click', () => {
        document.querySelector('#addContactBtn').remove();
        const newContactName = document.createElement('INPUT');
        newContactName.type = 'text';
        newContactName.classList = ('form-control mb-3');
        newContactName.placeholder = 'Name';

        const newContsaveBtn = document.createElement('button');
        newContsaveBtn.innerHTML = 'Save';
        newContsaveBtn.classList = ('btn btn-primary m-2 mb-3');
        const newContcancelBtn = document.createElement('button');
        newContcancelBtn.innerHTML = 'Cancel';
        newContcancelBtn.classList = ('btn btn-primary m-2 mb-3');

        document.querySelector('#addContactFormBox').append(newContactName, newContsaveBtn, newContcancelBtn);

        newContcancelBtn.addEventListener('click', () => {location.reload()});
        newContsaveBtn.addEventListener('click', () => {
            if(newContactName.value) {
                // upload new contact info 
                const request = new Request(
                    '/add_contact/',
                    {headers: {'X-CSRFToken': csrftoken}}
                );
                fetch(request, {
                    method: 'POST',
                    mode: 'same-origin',
                    body: JSON.stringify({
                        contact: newContactName.value,
                    })
                }).then(response => response.json())
                .then(result => {
                    if (result.error === 'user not found') {
                        alert('User not found')
                    }
                    else {
                        window.location.reload();
                        alert('Contact added')
                    }
                });
            }
            else {
                alert('You must provide name and account number')
            }
        });
    })

})



const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
})

let current_user = ''

// -----------------------
let balanceField = document.querySelector('#balanceField')
document.addEventListener('DOMContentLoaded', () => {
    fetch('get_balance/')
    .then(response => response.json())
    .then(user => {
        balanceField.innerHTML = `<strong>${formatter.format(user.balance)}</strong>`;
    })

    fetch('get_contacts/')
    .then(response => response.json())
    .then(contacts => {
        for (let i = 0; i < contacts.length; i++) {
            const option = document.createElement('option');
            option.value = contacts[i].contact;
            option.innerHTML = contacts[i].contact;
            document.querySelector('#avlbReceiver').append(option)
        }
    });


    fetch('get_user/')
    .then(response => response.json())
    .then(user => {
        current_user = user;
    })


    fetch('get_transactions/')
    .then(response => response.json())
    .then(transactions => {
        for (let i = 0; i < transactions.length; i++) {
            // add transactions to the page
            let transaction = transactions[i];
            const element = document.createElement('div');
            element.classList = ('card mb-3 padding')
            if (current_user.user === transaction.sender && current_user.user === transaction.receiver) {
                element.innerHTML = `<strong>${formatter.format(transaction.amount)}</strong>DEPOSIT CASH<br> <div class="ms-auto">${transaction.timestamp}</div>`;
                element.style.background='#B9FCA0';
            }
            else if(current_user.user === transaction.sender) {
                element.innerHTML = `<strong>${formatter.format(transaction.amount)}</strong>${current_user.user} >>> ${transaction.receiver}<br> <div class="ms-auto">${transaction.timestamp}</div>`;
                element.style.background='#FCA0A0';
            }
            else {
                element.innerHTML = `<strong>${formatter.format(transaction.amount)}</strong>${current_user.user} <<< ${transaction.sender}<br> <div class="ms-auto">${transaction.timestamp}</div>`;
                element.style.background='#B9FCA0';
            }
            
            document.querySelector('#transactionsList').append(element)
        }
    });
})


document.querySelector('#addCashBtn').addEventListener('click', () => {
    document.querySelector('#addCashBtn').style.display = 'none';
    const cashAmount = document.createElement('INPUT');
    cashAmount.placeholder = 'Amount';
    cashAmount.type = 'number';
    cashAmount.step = '0.01';
    cashAmount.classList = ('form-control')
    const cancel = document.createElement('button');
    cancel.classList = ('btn btn-primary m-2 padding');
    cancel.innerHTML = 'Cancel';
    const add = document.createElement('button');
    add.classList = ('btn btn-primary m-2 padding');
    add.innerHTML = 'Add Cash';
    cancel.addEventListener('click', () => {window.location.reload();})
    document.querySelector('#addCashForm').append(cashAmount, cancel, add);
    add.addEventListener('click', () => {
        if (cashAmount.value && cashAmount.value > 0) {
            // add cash
            const request = new Request(
                '/add_cash/',
                {headers: {'X-CSRFToken': csrftoken}}
            );
            fetch(request, {
                method: 'POST',
                mode: 'same-origin',
                body: JSON.stringify({
                    amount: cashAmount.value,
                })
            }).then(response => response.json())
            .then(result => {
                if (result.error === 'something went wrong') {
                    alert('Something went wrong')
                }
                else {
                    window.location.reload();
                    alert('Cash added')
                }
            });
        } else {
            alert('Amount not valid')
        }
    })
})