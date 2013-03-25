;; ====================== Global  Thingies ====================== ;;

;; Add ~/.emacs.d/elisp/ to the load-path
(add-to-list 'load-path "~/.emacs.d/elisp/")

;; Create the autosave dir if necessary, since emacs won't.
(make-directory "~/.emacs.d/autosaves/" t)

;; Create the backup dir if necessary, since emacs won't
(make-directory "~/.emacs.d/backups/" t)

;; Set autosave directory
;; Set backup directory
;; Disable initial splash
;; Show Matching parentheses
(custom-set-variables
  ;; custom-set-variables was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 '(auto-save-file-name-transforms (quote ((".*" "~/.emacs.d/autosaves/\\1" t))))
 '(backup-directory-alist (quote ((".*" . "~/.emacs.d/backups/"))))
 '(inhibit-startup-screen t)
 '(show-paren-mode t))
(custom-set-faces
 )

;; ==================== Make Tab Four Spaces ==================== ;; 

;; Change the indentation amount to 4 spaces instead of 2.
;; You have to do it in this complicated way because of the
;; strange way the cc-mode initializes the value of `c-basic-offset'.
(add-hook 'c-mode-hook (lambda () (setq c-basic-offset 4)))

;; Additional Tab Functions (Replace tabs with spaces, Set width to 4)
(setq-default indent-tabs-mode nil)
(setq-default tab-width 4)


;; ====================    Duplicate Line    ==================== ;;

;; Duplicate line on C-c C-c C-d
(global-set-key "\C-c\C-c\C-d" "\C-a\C- \C-n\M-w\C-y")

;; ====================  Misc Functionality  ==================== ;;

;; Make the sequence "C-x w" execute the `what-line' command, 
;; which prints the current line number in the echo area.
(global-set-key "\C-xw" 'what-line)

;; Make F1 invoke help
(global-set-key [f1] 'help-command)
;; Make F2 be `undo'
(global-set-key [f2] 'undo)
;; Make F3 be `find-file'
;; Note: it does not currently work to say
;;   (global-set-key 'f3 "\C-x\C-f")
;; The reason is that macros can't do interactive things properly.
;; This is an extremely longstanding bug in Emacs.  Eventually,
;; it will be fixed. (Hopefully ..)
(global-set-key [f3] 'find-file)

;; Make F4 be "mark", F5 be "copy", F6 be "paste"
;; Note that you can set a key sequence either to a command or to another
;; key sequence.
(global-set-key [f4] 'set-mark-command)
(global-set-key [f5] "\M-w")
(global-set-key [f6] "\C-y")

;; Reload a File
(global-set-key "\C-c\C-r" 'reload-file)

;; Set up aspell to replace ispell
(setq-default ispell-program-name "aspell")

;; ====================   Language   Hooks   ==================== ;;

;; LUA mode
(setq auto-mode-alist (cons '("\.lua$" . lua-mode) auto-mode-alist))
(autoload 'lua-mode "lua-mode" "Lua editing mode." t)

;; Python Mode
(autoload 'python-mode "python-mode.el" "Python mode." t)
(setq auto-mode-alist (append '(("/*.\.py$" . python-mode)) auto-mode-alist))

;; Lisp Settings
(show-paren-mode)

;; Load AUCTeX
(load "auctex.el" nil t t)
(load "preview-latex.el" nil t t)

;; Web-Mode
(require 'web-mode)
(add-to-list 'auto-mode-alist '("\\.phtml\\'" . web-mode))
(add-to-list 'auto-mode-alist '("\\.tpl\\'" . web-mode))
(add-to-list 'auto-mode-alist '("\\.php\\'" . web-mode))
(add-to-list 'auto-mode-alist '("\\.jsp\\'" . web-mode))
(add-to-list 'auto-mode-alist '("\\.as[cp]x\\'" . web-mode))
(add-to-list 'auto-mode-alist '("\\.erb\\'" . web-mode))
(add-to-list 'auto-mode-alist '("\\.mustache\\'" . web-mode))
(add-to-list 'auto-mode-alist '("\\.djhtml\\'" . web-mode))

;; Additional modes

;; ====================  Window  Properties  ==================== ;;

;; Line numbers in fringe
(global-linum-mode 1)

;; Default to wrap at buffer edge
(global-visual-line-mode 1)

;; Disable scrollbars, menubars, and toolbars
(scroll-bar-mode 0)
(menu-bar-mode 0)
(tool-bar-mode 0)

;; ====================     Color Themes     ==================== ;;

(require 'color-theme)
(color-theme-initialize)
(color-theme-oswald)

;; ====================  Set Email Address   ==================== ;;

(setq user-mail-address "larset2@gmail.com")

