(ns clojure-quirk.core 
  (:use clojure.pprint)    
  (:require [instaparse.core :as insta]))

         

;; start utilities
(defn CallBylabel [funLabel & args]
  (apply (ns-resolve 'clojure-quirk.core (symbol (name funLabel))) args))

(defn godown [pt index scope]
  (let [st (pt index)]
    (CallBylabel (st 0) st scope)))

(defn root [pt]
  ((pt 1) 0))

(defn ret-print [thingToPrint] 
  (println thingToPrint)
  thingToPrint)
;; end utilities

;; <Program> -> <Statement> <Program> | <Statement>
(defn Program [pt scope]
  (if (> (count pt) 2)
    (godown pt 2 (godown pt 1 scope))
    (godown pt 1 scope)))
  
;; <Statement> -> <FunctionDeclaration> | <Assignment> | <Print>
(defn Statement [pt scope]
  (godown pt 1 scope))

;; <FunctionDeclaration> -> FUNCTION <Name> LPAREN <FunctionParams> LBRACE <FunctionBody> RBRACE
(defn FunctionDeclaration [pt scope]
  (let [functionName (godown pt 2 scope)
        paramNames (godown pt 4 scope)]
    (assoc scope functionName [paramNames (pt 6)] )))
  
;; <FunctionParams> -> <NameList> RPAREN | RPAREN
;; should return a list of values
(defn FunctionParams [pt scope]
  (if ( > (count pt) 2)
    (godown pt 1 scope)
    nil))

;; <FunctionBody> -> <Program> <Return> | <Return>
(defn FunctionBody [pt scope]
  (if (> (count pt) 2)
   ([(pt 1) (pt 2)])
    (pt 1)))

;; <Return> -> RETURN <ParameterList>
(defn Return [pt scope]
    (godown pt 2 scope))

;; <Assignment> -> <SingleAssignment> | <MultipleAssignment>
(defn Assignment [pt scope]
   (godown pt 1 scope))

;; <SingleAssignment> -> VAR <Name> ASSIGN <Expression>
(defn SingleAssignment [pt scope]
  (let [name (godown pt 2 scope)
        value (godown pt 4 scope)]
    (assoc scope name value)))

;; <MultipleAssignment> -> VAR <NameList> ASSIGN <FunctionCall>
(defn MultipleAssignment [pt scope]
  (let [list (godown pt 2 scope)
        values (godown pt 4 scope)]
    (merge scope (zipmap list values))))

;; <Print> -> PRINT <Expression>
(defn Print [pt, scope]
  (let [val (godown pt 2 scope)]
    (if (number? val)
      (println val)
      (println (clojure.string/join ", "  val)))
    scope))

;; <NameList> -> <Name> COMMA <NameList> | <Name>
(defn NameList [pt scope]
  (if ( > (count  pt) 2)
    (let [name (godown pt 1 scope)
          list (godown pt 3 scope)]
    (into [name] list))
    [(godown pt 1 scope)]))
  
;; <ParameterList> -> <Parameter> COMMA <ParameterList> | <Parameter>
;; should return a a list of values.
(defn ParameterList [pt scope]
  (if ( > (count  pt) 2)
    (let [name (godown pt 1 scope)
          list (godown pt 3 scope)]
      (into [name] list))
    [(godown pt 1 scope)]))

;; <Parameter> -> <Expression> | <Name>
(defn Parameter [pt scope]
  (godown pt 1 scope))
  
;; <Expression> -> <Term> ADD <Expression> | <Term> SUB <Expression> | <Term>
(defn Expression [pt scope]
  (if (> (count pt) 2)
    (let [lval (godown pt 1 scope)
          rval (godown pt 3 scope)]
    (if (= :ADD ((pt 2) 0))
      (+ lval rval)
      (- lval rval)))
    (godown pt 1 scope)))

;; <Term> -> <Factor> MULT <Term> | <Factor> DIV <Term> | <Factor>
(defn Term [pt scope]
  (if (> (count pt) 2)
    (let [lval (godown pt 1 scope)
          rval (godown pt 3 scope)]
    (if (= :MULT ((pt 2) 0))
      (* lval rval)
      (/ lval rval)))
    (godown pt 1 scope)))

;; <Factor> -> <SubExpression> EXP <Factor> | <SubExpression> | <FunctionCall> | <Value> EXP <Factor> | <Value>
(defn Factor [pt scope]
  (if (> (count pt) 2)
  (let [lval (godown pt 1 scope)
        rval (godown pt 3 scope)]
    (Math/pow lval rval))
  (godown pt 1 scope)))

;; <FunctionCall> ->  <Name> LPAREN <FunctionCallParams> COLON <Number> | <Name> LPAREN <FunctionCallParams>
(defn FunctionCall [pt scope]
  (let [func (godown pt 1 scope)
        nscope (assoc {} :__parent__ scope)
        pnames (func 0)
        pvalues (godown pt 3 scope)
        nscope (merge nscope (zipmap pnames pvalues))
        body (func 1)
        return (Program body nscope)
        ]
    (if (> (count pt) 5)
      (let [index (int (godown pt 5 scope))]
           (vector (return index)))
      return)))

;; <FunctionCallParams> ->  <ParameterList> RPAREN | RPAREN
(defn FunctionCallParams [pt scope]
  (if (> (count pt) 2)
    (godown pt 1 scope)
    nil))

;; <SubExpression> -> LPAREN <Expression> RPAREN
(defn SubExpression [pt scope]
  (godown pt 2 scope))

;; <Value> -> <Name> | <Number>
(defn Value [pt scope]
  (godown pt 1 scope))

;; <Name> -> IDENT | SUB IDENT | ADD IDENT
(defn Name [pt scope]
  (letfn 
    [(getI [x] (scope (keyword x)))
     (ret [y] (if (contains? scope (keyword y))
                (getI y)
                (keyword y)))]
    (case (root pt)
      :SUB (- (getI ((pt 2) 1)))
      :ADD (getI ((pt 2) 1))
      (ret ((pt 1) 1)))))

;; <Number> -> NUMBER | SUB NUMBER | ADD NUMBER
(defn MyNumber [pt scope]
  (letfn [(pd [x] (Double/parseDouble x))]
    (case (root pt)
      :SUB (- (pd ((pt 2) 1)))
      :ADD (pd ((pt 2) 1))
      (pd ((pt 1) 1)))))

(defn -main [& args]
  (def quirk
    (insta/parser (slurp "resources/grammer.txt")))
  
 (def program-tree 
   (quirk (slurp *in*)))
 
 (def SHOW_PARSE_TREE
   (= "-pt" (first *command-line-args*))) 

  (if SHOW_PARSE_TREE
     (pprint program-tree)
     (Program program-tree {})))
