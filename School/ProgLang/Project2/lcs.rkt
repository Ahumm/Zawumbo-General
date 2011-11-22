;; Tate Larsen
;; Prog Lang
;; Project 2: SCHEME
;; Part 2


;;;;;;;;;; LCS_SLOW ;;;;;;;;;;
;; Complexity is O(2^n) so  ;;
;;  this algorithm becomes  ;;
;;  unbearably slow quickly ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Contract: lcs_slow : list list -> list
;; Purpose: finds a longest common subsequence of a and b or '() if none exists
;; Example: (lcs_slow '(1 2 3) '(2 3 4)) should return (2 3)
;; Definition:
(define (lcs_slow a b)
   (slow_runner a b (minimum (len a) (len b))))

;; Contract: slow_runner : list list number -> list
;; Purpose: finds a longest common subsequence of a and b of length l or smaller or '() if none exists
;; Example: (slow_runner '(1 2 3) '(2 3 4) 2) should return (2 3)
;; Definition:
(define (slow_runner a b l)
    (if (equal? l 0) '() 
       (if (equal? (slow_processor (sub_generator a l) (sub_generator b l) l) '())
          (slow_runner a b (- l 1))
          (slow_processor (sub_generator a l) (sub_generator b l) l))))

;; Contract: slow_processor : list list number -> list
;; Purpose: finds a longest common subsequence of a and b of length l or '() if none exists
;; Example: (slow_processor '(1 2 3) '(2 3 4) 2) should return (2 3)
;; Definition:
(define (slow_processor a b l)
   (if (equal? a '())
      '()
      (if (equal? b '())
         '()
         (if (equal? (contains (car a) b) '())
            (if (equal? (contains (car b) a) '())
               (slow_runner (cdr a) (cdr b) l)
               (contains (car b) a))
            (contains (car a) b)))))
         

;;;;;;;;;; LCS_FAST ;;;;;;;;;;
;; Complexity: O(m*n) where ;;
;;  m and n are the lengths ;;
;;  of the lists. Passes    ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Contract: lcs_fast : list list -> list
;; Purpose: finds a longest common subsequence of a and b or '() if none exists
;; Example: (lcs_fast '(1 2 3) '(2 3 4)) should return (2 3)
;; Definition:
(define (lcs_fast a b)
   (cond ((equal? a '()) '())
         ((equal? b '()) '())
         ((atom? a) (if (atom? b) (if (equal? a b) (list a) '()) (if (equal? a (contains a b)) (list a) '())))
         ((atom? b) (if (equal? b (contains b a)) (list b) '()))
         ((equal? (car a) (car b))
            (cons (car a) (lcs_fast (cdr a) (cdr b))))
         (else
            (if (eq? (minimum (len (lcs_fast a (cdr b))) (len (lcs_fast b (cdr a)))) (len (lcs_fast a (cdr b))))
               (lcs_fast b (cdr a))
               (lcs_fast a (cdr b))))))




;;;;;;;;;; UTILITY FUNCTIONS ;;;;;;;;;;

;; Contract: atom? : value -> boolean
;; Purpose: returns #t if x is not null, a list, or a pair, else false
;; Example: (atom? '(1 2 3) should return #f
;; Definition:
(define (atom? x) (not (or (pair? x) (null? x))))

;; Contract: contains : value list -> value
;; Purpose: returns a if a is an element of l
;; Example: (contains 3 '(1 2 3 4)) should return 3
;; Definition:
(define (contains a l)
   (if (equal? l '())
      '()
      (if (equal? a (car l))
         a
         (contains a (cdr l)))))

;; Contract: sub_generator : list number -> all subsequences of list of length i
;; Purpose: to find all possible subsequences of l of length i
;; Example: (sub_generator '(1 2 3 4) 2) should return ((1 2) (1 3) (1 4) (2 3) (2 4) (3 4))
;; Definition:
(define (sub_generator l i)
   (if (equal? 0 i)
      (list '())
      (if (equal? l '())
         '()
         (merge (cons_all (car l) (sub_generator (cdr l) (- i 1))) (sub_generator (cdr l) i)))))

;; Contract: cons_all : value list -> list
;; Purpose: appends a value to every list in a list of lists
;; Example: (cons_all 5 '('(1 2) '(3 4))) should return ((1 2 5) (3 4 5))
;; Definition:
(define (cons_all a l)
    (if (equal? l '())
       '()
       (cons (cons a (car l)) (cons_all a (cdr l)))))

;; Contract: merge : list list -> list
;; Purpose: merges two lists
;; Example: (merge (1 2) (3 4)) should return (1 2 3 4)
;; Definition:
(define (merge a b)
   (if (equal? a '())
      b
      (if (equal? b '())
         a
         (cons (car a) (merge (cdr a) b)))))
         
;; Contract: len : (list �a) -> integer
;; Purpose: to compute length of a list l
;; Example: (len �(1 (2 3) 4)) should return 3
;; Definition:
(define (len l)
   (if (null? l) 0 (+ 1 (len(cdr l)))))

;; Contract: minimum : number number -> number
;; Purpose: find the minumum of two numbers
;; Example: (minimum 1 2) should return 1
;; Definition:
(define (minimum x y)
   (if (< x y) x y))
   
;; Contract: maximum : number number -> number
;; Purpose: find the maxumum of two numbers
;; Example: (maximum 1 2) should return 2
;; Definition:
(define (maximum x y)
   (if (< x y) x y))

(define list1 '(a b c b d a b))
(define list2 '(b d c a b a))
;;(lcs_slow list1 list2)
(lcs_fast list1 list2)
