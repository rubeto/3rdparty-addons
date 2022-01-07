odoo.define("switch_user_app.UserMenu", function (require) {
  "use strict";

  var core = require("web.core");
  var framework = require("web.framework");
  var Dialog = require("web.Dialog");
  var Widget = require("web.Widget");
  var session = require("web.session");
  var Menu = require("web.WebClient");

  var _t = core._t;
  var QWeb = core.qweb;

  var UserMenu = require("web.UserMenu");

  UserMenu.include({
    _searchUserFetch: function (searchVal, limit, user_id) {
      let domain = [
        ["name", "ilike", searchVal],
        ["id", "!=", user_id],
      ];
      return this._rpc({
        model: "res.users",
        method: "search_read",
        domain: domain,
        fields: ["id", "name", "login", "display_name"],
        limit: limit || 20,
      });
    },

    searchUser: function (searchVal, limit, user_id) {
      let def = this._searchUserFetch(searchVal, limit, user_id);
      return def.then(function (users) {
        var suggestions = _.map(users, function (user) {
          return {
            id: user.id,
            value: user.login,
            label: user.name,
          };
        });
        return _.sortBy(suggestions, "label");
      });
    },

    _onMenuSwitch_user: function () {
      var self = this;
      var session = this.getSession();
      this.trigger_up("clear_uncommitted_changes", {
        callback: function () {
          let $optionsEl =
            '<div class="form-group">\
             <label class="col-form-label"  for="login_user">User</label>\
              <input type="text" class="o_input o_user_switch_input" id="login_user" name="login_user"/> \
             </div>';
          let passwordEl = "";
          if (session.switch_user_by_password) {
            passwordEl =
              '<div class="form-group">\
                  <label class="col-form-label"  for="password">Password</label>\
                  <input type="password" class="form-control" id="password" name="password" required="required"/>\
             </div>';
          }
          var $content = $("<div>").append(
            $(`${$optionsEl} ${passwordEl}</div>`)
          );

          let $partner_input = $content.find(".o_user_switch_input");
          $partner_input.select2({
            width: "100%",
            allowClear: true,
            //formatResult: function (item) {
            //  return $(`<span>`).text(item.text);
            //},
            query: function (query) {
              self
                .searchUser(query.term, 30, session.uid)
                .then(function (users) {
                  query.callback({
                    results: _.map(users, function (user) {
                      return _.extend(user, { text: user.label });
                    }),
                  });
                });
            },
          });
          if (session.switch_user_by_password) {
            return new Dialog(this, {
              title: _t("Switch User"),
              buttons: [
                {
                  text: _t("Switch"),
                  classes: "btn-primary",
                  //close: true,
                  click: function () {
                    var new_user = this.$content.find("#login_user").val();
                    var password = this.$content.find("#password").val();
                    if (new_user && password) {
                      let params = {
                        db: session.db,
                        user: new_user,
                        password: password,
                      };
                      return self
                        ._rpc({
                          route: "/web/switch_user/authenticate/",
                          params,
                        })
                        .then(function (result) {
                          if (!result.uid) {
                            return $.Deferred().reject();
                          } else {
                            window.location = result["web.base.url"];
                          }
                        });
                    } else {
                      let msg = `${
                        !new_user
                          ? "Please Choose User!"
                          : !password
                          ? "Please Entere Password!"
                          : ""
                      }`;
                      Dialog.alert(self, _t(msg), {
                        title: _t("Inputs"),
                      });
                    }
                  },
                },
                { text: _t("Discard"), close: true },
              ],
              $content: $content,
            }).open();
          } else {
            return new Dialog(this, {
              title: _t("Switch User"),
              buttons: [
                {
                  text: _t("Switch"),
                  classes: "btn-primary",
                  //close: true,
                  click: function () {
                    var new_user = this.$content.find("#login_user").val();
                    var password = "pass";
                    if (new_user) {
                      let params = {
                        db: session.db,
                        user: new_user,
                        password: password,
                      };
                      return self
                        ._rpc({
                          route: "/web/switch_user/authenticate/",
                          params,
                        })
                        .then(function (result) {
                          if (!result.uid) {
                            return $.Deferred().reject();
                          } else {
                            window.location = result["web.base.url"];
                          }
                        });
                    } else {
                      let msg = `${!new_user ? "Please Choose User!" : ""}`;
                      Dialog.alert(self, _t(msg), {
                        title: _t("Inputs"),
                      });
                    }
                  },
                },
                { text: _t("Discard"), close: true },
              ],
              $content: $content,
            }).open();
          }
        },
      });
    },
  });
});
