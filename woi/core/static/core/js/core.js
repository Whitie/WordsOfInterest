const woi_js = JSON.parse(document.getElementById('woi-js').textContent);

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

function _mark_as_read(url) {
    m.request({
        method: 'GET',
        url: url
    }).then(function(res) {
        let date = new Date();
        localStorage.setItem(url, date.toLocaleString());
    });
}

function mark_as_read(url) {
    let date = localStorage.getItem(url);
    if (date === null) {
        window.setTimeout(_mark_as_read, 10000, url);
    }
    return date;
}

document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
      const $notification = $delete.parentNode;
      $delete.addEventListener('click', () => {
        $notification.parentNode.removeChild($notification);
      });
    });
    (document.querySelectorAll('.woi-article') || []).forEach((element) => {
        let view_url = element.dataset.viewurl;
        let post_id = element.dataset.postid;
        let seen = localStorage.getItem(view_url);
        if (seen !== null) {
          let pos = document.getElementById('seen-' + post_id);
          m.render(pos, [
            m('i.fas.fa-grip-lines-vertical'),
            m('span.has-text-link', {title: gettext('Read on')}, [
              m('span.icon', m('i.far.fa-eye')),
              m('span', seen)
            ])
          ]);
        }
    });
});

var Panels = {
    left: {
        list: [],
        fetch: function() {
        m.request({
            method: 'GET',
            url: woi_js.left_url,
            withCredentials: true
        }).then(function(result) {
            Panels.left.list = result.data;
        })
        }
    },
    right: {
        list: [],
        fetch: function() {
        m.request({
            method: 'GET',
            url: woi_js.right_url,
            withCredentials: true
        }).then(function(result) {
            Panels.right.list = result.data;
        })
        }
    }
};

var Comment = {
    data: {
        name: '',
        email: '',
        body: '',
        post_id: null
    },
    save: function() {
        return m.request({
            method: 'PUT',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            url: woi_js.save_comment_url,
            body: Comment.data
        });
    }
};

var CommentForm = {
    view: function() {
        return m('div.media-content', 
            m('form', {
                onsubmit: function(e) {
                    e.preventDefault();
                    Comment.save().then(function(res) {
                        count++;
                        Comment.data.name = '';
                        Comment.data.email = '';
                        Comment.data.body = '';
                    });
                }
            }, [
                m('div.field.is-horizontal',
                    m('div.field-body', [
                        m('div.field',
                            m('p.control.is-expanded.has-icons-left', [
                                m('input.input.is-success[type=text][required]', {
                                    placeholder: gettext('Name'),
                                    value: Comment.data.name,
                                    oninput: function(e) {
                                        Comment.data.name = e.target.value;
                                    }
                                }),
                                m('span.icon.is-small.is-left', m('i.fas.fa-user'))    
                            ])),
                        m('div.field',
                            m('p.control.is-expanded.has-icons-left', [
                                m('input.input[type=email]', {
                                    placeholder: gettext('Email (optional)'),
                                    value: Comment.data.email,
                                    title: gettext('Not published, only visible for the author of the article.'),
                                    oninput: function(e) {
                                        Comment.data.email = e.target.value;
                                    }
                                }),
                                m('span.icon.is-small.is-left', m('i.fas.fa-envelope'))
                            ]))
                    ])
                ),
                m('div.field',
                    m('p.control',
                        m('textarea.textarea.is-success[required]', {
                            placeholder: gettext('Your text...'),
                            value: Comment.data.body,
                            oninput: function(e) {
                                Comment.data.body = e.target.value;
                            }
                        })
                    )
                ),
                m('div.field',
                    m('p.control',
                        m('button.button.is-primary', [
                            m('span.icon', m('i.far.fa-paper-plane')),
                            m('span', gettext('Post comment'))
                        ])
                    )
                )
            ])
        );
    }
};

let div_left = document.getElementById('left');
let div_right = document.getElementById('right');
if (div_left) {
    var Left = {
        oninit: Panels.left.fetch,
        view: function(vnode) {
        return Panels.left.list.map(function(item) {
            return m('div.box.content', {id: item.id}, m.trust(item.content))
        })
        }
    }
    m.mount(div_left, Left);
};
if (div_right) {
    var Right = {
        oninit: Panels.right.fetch,
        view: function(vnode) {
        return Panels.right.list.map(function(item) {
            return m('div.box.content', {id: item.id}, m.trust(item.content))
        })
        }
    }
    m.mount(div_right, Right);
};
